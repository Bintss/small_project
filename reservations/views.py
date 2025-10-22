# reservations/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ReservationSerializer
from .models import Reservation
from gyms.models import Court
import datetime

class AvailableSlotsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # 1. 쿼리 파라미터를 받습니다.
        court_id = request.query_params.get('court_id')
        date_str = request.query_params.get('date')

        if not court_id or not date_str:
            return Response({"error": "court_id와 date는 필수 파라미터입니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reservation_date = datetime.date.fromisoformat(date_str)
        except ValueError:
            return Response({"error": "날짜 형식이 올바르지 않습니다. (YYYY-MM-DD)"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. 모든 1시간 단위 '시작' 슬롯을 정의 (09:00 ~ 21:00)
        all_slots_times = [datetime.time(hour=h) for h in range(0, 24)]

        try:
            # 3. (핵심) DB에서 해당 날짜의 모든 예약을 '한 번만' 가져옵니다.
            existing_reservations = Reservation.objects.filter(
                court_id=court_id,
                reservation_date=reservation_date
            )

            available_slots = []

            # 4. (핵심) 09시부터 21시까지 1시간 단위로 루프를 돕니다.
            for potential_start in all_slots_times:
                # 1시간 뒤 시간을 계산 (예: 09:00 -> 10:00)
                potential_end = (datetime.datetime.combine(datetime.date.today(), potential_start) + 
                                 datetime.timedelta(hours=1)).time()

                is_slot_available = True

                # 5. 이 1시간 슬롯이, 기존 예약 중 하나라도 겹치는지 확인합니다.
                for old_res in existing_reservations:
                    # (기존 예약 시작 < 1시간 슬롯 끝) AND (기존 예약 끝 > 1시간 슬롯 시작)
                    if (old_res.start_time < potential_end) and (old_res.end_time > potential_start):
                        is_slot_available = False
                        break # 이미 겹쳤으니 더 이상 확인할 필요 없음

                # 6. 겹치는 예약이 하나도 없었다면, 이 슬롯은 예약 가능!
                if is_slot_available:
                    available_slots.append(potential_start)

            # 7. 사용자에게는 다시 문자열로 변환하여 반환
            available_slots_str = [t.strftime('%H:%M:%S') for t in available_slots]

            return Response({"available_slots": available_slots_str}, status=status.HTTP_200_OK)

        except Court.DoesNotExist:
            return Response({"error": "존재하지 않는 코트입니다."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ReservationCreateView       
class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated] # 반드시 로그인한 사용자만 예약 가능!

    def perform_create(self, serializer):
        # Serializer가 예약을 저장(create)할 때,
        # user 필드를 현재 로그인한 사용자로 자동 설정
        serializer.save(user=self.request.user)