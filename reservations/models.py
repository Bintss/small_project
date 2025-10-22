# reservations/models.py
from django.db import models
from django.conf import settings
from gyms.models import Court

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='reservations')

    reservation_date = models.DateField() # 예약 날짜 (예: 2025-10-26)
    start_time = models.TimeField()       # 시작 시간 (예: 09:00:00)
    end_time = models.TimeField()         # 종료 시간 (예: 10:00:00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 한 사용자가 특정 코트의 특정 날짜와 시작 시간을 중복 예약할 수 없도록 설정
        unique_together = ('court', 'reservation_date', 'start_time')

    def __str__(self):
        return f'{self.user.name} - {self.court.name} ({self.reservation_date} {self.start_time})'