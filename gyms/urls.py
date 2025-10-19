# gyms/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourtViewSet, GymViewSet # GymCreateView는 이제 사용 안 함

router = DefaultRouter()
# /gyms 주소에 GymViewSet을 등록. 이제 GET, POST, PUT, DELETE 모두 처리
router.register(r'gyms', GymViewSet, basename='gym')

urlpatterns = [
    path('', include(router.urls)),
    # 아래는 코트 관련 URL들 (기존과 동일)
    path('gyms/<int:gym_pk>/courts/', CourtViewSet.as_view({'get': 'list', 'post': 'create'}), name='court-list'),
    path('gyms/<int:gym_pk>/courts/<int:pk>/', CourtViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='court-detail'),
]