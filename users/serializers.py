# users/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__' # 모든 필드를 포함할 경우
        fields = ['id', 'email', 'name', 'password'] # 필요한 필드만 지정
        extra_kwargs = {
            # password는 쓰기 전용으로 설정하고, 응답에는 포함시키지 않음
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # User 모델의 create_user 헬퍼 메소드를 사용하여 사용자를 생성
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user