from django.shortcuts import render

# users/views.py
from .models import User
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework import permissions


# generics.CreateAPIView를 상속받아 create(회원가입) 기능만 특화된 View 작성
class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# 정보조회
class MyProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] # 오직 인증된 사용자만 접근 가능!

    def get_object(self):
        # 요청을 보낸 사용자(request.user) 객체를 반환
        return self.request.user