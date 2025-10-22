# reservations/serializers.py
from rest_framework import serializers
from .models import Reservation
import datetime
from gyms.serializers import CourtSerializer

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        # 'user'는 자동으로 채우고, 'end_time'도 이제 사용자에게 직접 입력받음
        fields = ['id', 'court', 'reservation_date', 'start_time', 'end_time', 'user']
        read_only_fields = ['user'] # end_time을 read_only에서 제거!

    def create(self, validated_data):
        # 1. (변경) create 메소드가 매우 단순해졌습니다.
        #    start_time, end_time 모두 사용자가 입력한 값(validated_data)을 그대로 사용합니다.
        #    user는 view에서 전달받아 자동으로 채워집니다.
        reservation = Reservation.objects.create(**validated_data)
        return reservation

    def validate(self, data):
        # 2. (추가) 시작 시간이 종료 시간보다 빠른지 확인합니다.
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("종료 시간은 시작 시간보다 늦어야 합니다.")

        # 3. (핵심 변경) 강력한 중복 예약 검증 로직
        #
        # 사용자가 요청한 시간 범위: [ New.start_time ] --- [ New.end_time ]
        # 기존에 DB에 있는 시간 범위:   [ Old.start_time ] --- [ Old.end_time ]
        #
        # 겹치는 경우는 (Old.start < New.end) AND (Old.end > New.start) 입니다.

        overlapping_reservations = Reservation.objects.filter(
            court=data['court'],
            reservation_date=data['reservation_date'],
            start_time__lt=data['end_time'], # 기존 예약의 시작시간 < 새 예약의 종료시간
            end_time__gt=data['start_time']   # 기존 예약의 종료시간 > 새 예약의 시작시간
        )

        if overlapping_reservations.exists():
            raise serializers.ValidationError("요청한 시간대에 이미 다른 예약이 존재합니다.")

        return data
    
# MyReservationListSerializer
class MyReservationListSerializer(serializers.ModelSerializer):
    # court 필드를 단순 ID가 아닌, CourtSerializer의 '중첩된' 정보로 보여줍니다.
    court = CourtSerializer(read_only=True)

    class Meta:
        model = Reservation
        # 응답으로 보여줄 필드들을 지정
        fields = ['id', 'court', 'reservation_date', 'start_time', 'end_time']