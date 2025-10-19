from django.shortcuts import render

# gyms/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Gym
from .serializers import GymSerializer

class GymCreateView(generics.CreateAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    permission_classes = [IsAuthenticated] # 오직 인증된 사용자만 체육관을 등록할 수 있음

    def perform_create(self, serializer):
        # serializer.save()가 호출될 때, owner 필드를 현재 로그인한 사용자로 자동 설정
        serializer.save(owner=self.request.user)