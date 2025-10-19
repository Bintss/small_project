from django.shortcuts import render

# gyms/views.py
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Gym, Court
from .serializers import GymSerializer, CourtSerializer, GymListSerializer, GymDetailSerializer
from .permissions import IsGymOwner


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

# GymViewSet
class GymViewSet(viewsets.ModelViewSet): # ReadOnlyModelViewSet -> ModelViewSet으로 변경
    queryset = Gym.objects.all()

    # 어떤 Serializer를 쓸지 결정
    def get_serializer_class(self):
        if self.action == 'list':
            return GymListSerializer
        elif self.action == 'retrieve':
            return GymDetailSerializer
        # 생성(create) 시에는 기존의 GymSerializer를 사용
        return GymSerializer

    # 어떤 권한을 적용할지 결정
    def get_permissions(self):
        if self.action in ['list', 'retrieve']: # 목록/상세 조회는
            permission_classes = [AllowAny] # 누구나 허용
        else: # 그 외(생성, 수정, 삭제)는
            permission_classes = [IsAuthenticated] # 로그인한 사용자만 허용
        return [permission() for permission in permission_classes]

    # 생성(create) 시 owner를 현재 사용자로 자동 설정
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)