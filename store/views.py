import re
import requests
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Developer, Application
from .serializers import DeveloperSerializer

APP_STORE_LOOKUP_URL = "https://itunes.apple.com/lookup"

class DeveloperCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeveloperSerializer

    def post(self, request, *args, **kwargs):
        url = request.data.get('url')
        if not url:
            return Response({"error": "URLが必要です"}, status=status.HTTP_400_BAD_REQUEST)

        match = re.search(r'id(\d+)', url)
        if not match:
            return Response({"error": "有効なappIdがURLに含まれていません"}, status=status.HTTP_400_BAD_REQUEST)

        app_id = match.group(1)
        response = requests.get(APP_STORE_LOOKUP_URL, params={'id': app_id, 'country': 'JP'})
        if response.status_code != 200:
            return Response({"error": "App Store APIエラー"}, status=status.HTTP_400_BAD_REQUEST)

        data = response.json()
        if data.get('resultCount') == 0:
            return Response({"error": "アプリ情報が見つかりません"}, status=status.HTTP_404_NOT_FOUND)

        app_data = data['results'][0]
        artist_id = app_data.get('artistId')
        artist_name = app_data.get('artistName')

        if Developer.objects.filter(artist_id=str(artist_id), user=request.user).exists():
            return Response({"error": "既にこのデベロッパーは登録済みです"}, status=status.HTTP_400_BAD_REQUEST)

        developer = Developer.objects.create(
            artist_id=str(artist_id),
            artist_name=artist_name,
            user=request.user
        )

        params = {'id': artist_id, 'entity': 'software', 'country': 'JP'}

        response_all = requests.get(APP_STORE_LOOKUP_URL, params=params)
        if response_all.status_code == 200:
            data_all = response_all.json()
            results = data_all.get('results', [])
            apps = results[1:] if len(results) > 1 else []
            for app in apps:
                Application.objects.create(
                    developer=developer,
                    track_name=app.get('trackName', ''),
                    track_url=app.get('trackViewUrl', ''),
                    genre=app.get('primaryGenreName', ''),
                    price=app.get('price', 0.0),
                    description=app.get('description', ''),
                    artworkUrl512=app.get('artworkUrl512', ''),
                    artworkUrl100=app.get('artworkUrl100', ''),
                    artworkUrl60=app.get('artworkUrl60', ''),
                    screenshotUrls=app.get('screenshotUrls', [])
                )
        else:
            print("アプリ情報の取得に失敗しました。")

        serializer = DeveloperSerializer(developer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DeveloperListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeveloperSerializer

    def get_queryset(self):
        return Developer.objects.filter(user=self.request.user)

class DeveloperDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer

class DeveloperDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeveloperSerializer
    def get_queryset(self):
        return Developer.objects.filter(user=self.request.user)
