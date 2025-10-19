# gyms/serializers.py
from rest_framework import serializers
from .models import Gym

class GymSerializer(serializers.ModelSerializer):
    # owner 필드를 응답에 표시할 때, 사용자의 이메일 주소를 보여줌 (읽기 전용)
    owner_email = serializers.EmailField(source='owner.email', read_only=True)

    class Meta:
        model = Gym
        # API를 통해 다룰 필드들을 명시
        fields = ['id', 'name', 'address', 'phone_number', 'description', 'owner', 'owner_email']
        # owner 필드는 직접 입력받지 않고, 요청을 보낸 사용자로 자동 설정할 것이므로 읽기 전용으로 만듦
        read_only_fields = ['owner']