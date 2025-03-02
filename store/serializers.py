from rest_framework import serializers
from .models import Developer, Application

# アプリ情報シリアライザ
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            price = float(instance.price)
        except Exception:
            price = 0
        int_price = int(price)  # 小数点以下を切り捨て
        data['price'] = "無料" if int_price == 0 else str(int_price)
        return data

# 開発者情報シリアライザ（アプリ情報もネスト）
class DeveloperSerializer(serializers.ModelSerializer):
    applications = ApplicationSerializer(many=True, read_only=True)

    class Meta:
        model = Developer
        fields = '__all__'
