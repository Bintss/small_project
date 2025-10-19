from django.shortcuts import render

# gyms/views.py
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Gym, Court
from .serializers import GymSerializer, CourtSerializer
from .permissions import IsGymOwner

class GymCreateView(generics.CreateAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    permission_classes = [IsAuthenticated] # 오직 인증된 사용자만 체육관을 등록할 수 있음

    def perform_create(self, serializer):
        # serializer.save()가 호출될 때, owner 필드를 현재 로그인한 사용자로 자동 설정
        serializer.save(owner=self.request.user)

# CourtViewSet
class CourtViewSet(viewsets.ModelViewSet):
    queryset = Court.objects.all()
    serializer_class = CourtSerializer
    permission_classes = [IsAuthenticated, IsGymOwner] # 로그인 + 체육관 주인 권한 필요

    def get_queryset(self):
        # URL로부터 gym_pk(체육관 ID)를 받아, 해당 체육관의 코트만 필터링
        return Court.objects.filter(gym_id=self.kwargs['gym_pk'])

    def perform_create(self, serializer):
        # URL로부터 gym_pk를 받아, 해당 체육관을 찾아 코트의 gym 필드를 자동 설정
        gym = Gym.objects.get(pk=self.kwargs['gym_pk'])
        self.check_object_permissions(self.request, gym) # IsGymOwner 권한 확인
        serializer.save(gym=gym)