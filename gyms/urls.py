# gyms/urls.py
from django.urls import path
from .views import GymCreateView, CourtViewSet

# .as_view()와 딕셔너리를 사용해 HTTP 메소드와 ViewSet 동작을 연결합니다.
court_list = CourtViewSet.as_view({
    'get': 'list',      # GET 요청은 'list' (목록 조회) 동작으로
    'post': 'create'    # POST 요청은 'create' (생성) 동작으로
})

court_detail = CourtViewSet.as_view({
    'get': 'retrieve',  # GET 요청은 'retrieve' (상세 조회) 동작으로
    'put': 'update',    # PUT 요청은 'update' (수정) 동작으로
    'delete': 'destroy' # DELETE 요청은 'destroy' (삭제) 동작으로
})

urlpatterns = [
    # POST /api/gyms/ -> 체육관 생성
    path('gyms/', GymCreateView.as_view(), name='gym-create'),

    # GET, POST /api/gyms/<int:gym_pk>/courts/ -> 특정 체육관의 코트 목록 조회 및 생성
    path('gyms/<int:gym_pk>/courts/', court_list, name='court-list'),

    # GET, PUT, DELETE /api/gyms/<int:gym_pk>/courts/<int:pk>/ -> 특정 코트 상세 조회, 수정, 삭제
    path('gyms/<int:gym_pk>/courts/<int:pk>/', court_detail, name='court-detail'),
]