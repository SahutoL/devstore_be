from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import UserRegistrationSerializer, PushSubscriptionSerializer
from .models import CustomUser, PushSubscription

# ユーザー登録API
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

class PushSubscriptionView(APIView):
    """
    クライアントからのPush購読情報を登録するAPI
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = PushSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
