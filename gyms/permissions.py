# gyms/permissions.py
from rest_framework import permissions

class IsGymOwner(permissions.BasePermission):
    """
    요청을 보낸 사용자가 해당 체육관의 주인인지 확인하는 권한
    """
    def has_object_permission(self, request, view, obj):
        # 읽기 권한(GET, HEAD, OPTIONS)은 누구나 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 권한(POST, PUT, DELETE 등)은 체육관의 주인에게만 허용
        return obj.owner == request.user