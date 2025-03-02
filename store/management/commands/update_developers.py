import re
import requests
from django.core.management.base import BaseCommand
from store.models import Developer, Application
from django.conf import settings
from pywebpush import webpush, WebPushException
from users.models import PushSubscription

APP_STORE_LOOKUP_URL = "https://itunes.apple.com/lookup"

class Command(BaseCommand):
    help = "毎日DBに保存されているデベロッパーのアプリ情報を更新し、新しいアプリが追加された場合にプッシュ通知を送信する"

    def handle(self, *args, **options):
        self.stdout.write("デベロッパー更新処理開始")
        developers = Developer.objects.all()
        for developer in developers:
            artist_id = developer.artist_id

            params = {'id': artist_id, 'entity': 'software', 'country': 'JP'}
            response = requests.get(APP_STORE_LOOKUP_URL, params=params)
            if response.status_code != 200:
                self.stdout.write(f"Developer {developer.artist_name} の更新に失敗: APIエラー")
                continue

            data = response.json()
            results = data.get('results', [])
            if len(results) <= 1:
                self.stdout.write(f"Developer {developer.artist_name} のアプリ情報は更新不要")
                continue

            apps = results[1:]
            existing_app_names = set(developer.applications.values_list('track_name', flat=True))
            new_apps = []
            for app in apps:
                track_name = app.get('trackName', '')
                if track_name and track_name not in existing_app_names:
                    new_app = Application.objects.create(
                        developer=developer,
                        track_name=track_name,
                        track_url=app.get('trackViewUrl', ''),
                        genre=app.get('primaryGenreName', ''),
                        price=app.get('price', 0.0),
                        description=app.get('description', ''),
                        artworkUrl512=app.get('artworkUrl512', ''),
                        artworkUrl100=app.get('artworkUrl100', ''),
                        artworkUrl60=app.get('artworkUrl60', ''),
                        screenshotUrls=app.get('screenshotUrls', [])
                    )
                    new_apps.append(new_app)
            if new_apps:
                self.stdout.write(f"Developer {developer.artist_name} に新規アプリ {len(new_apps)} 件を追加")
                user = developer.user
                subscriptions = PushSubscription.objects.filter(user=user)
                payload = f"{developer.artist_name} の新しいアプリが追加されました！"
                for sub in subscriptions:
                    try:
                        webpush(
                            subscription_info={
                                "endpoint": sub.endpoint,
                                "keys": {
                                    "p256dh": sub.p256dh,
                                    "auth": sub.auth,
                                }
                            },
                            data=payload,
                            vapid_private_key=settings.VAPID_PRIVATE_KEY,
                            vapid_claims=settings.VAPID_CLAIMS
                        )
                        self.stdout.write(f"User {user.username} にプッシュ通知送信")
                    except WebPushException as ex:
                        self.stdout.write(f"プッシュ通知送信失敗: {ex}")
            else:
                self.stdout.write(f"Developer {developer.artist_name} には新規アプリはありません")
        self.stdout.write("デベロッパー更新処理終了")
