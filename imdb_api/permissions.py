from rest_framework import permissions

class AdminOrReadOnly(permissions.IsAdminUser):
    message = "You must be an admin to perform this action."

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        if request.method == 'GET' or is_admin:
            return True
        return False


class ReviewUserOrReadOnly(permissions.BasePermission):
    message = "You must be the owner of this review."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.review_user == request.user
        # else:
        #     if obj.review_user == request.user:
        #         return True
        #     else:
        #         return False