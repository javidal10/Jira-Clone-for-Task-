from django.urls import  path
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, IssueViewSet, ListViewSet, MemberViewSet, ProjectViewSet, UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'members', MemberViewSet, basename='member')
router.register(r'list', ListViewSet, basename='list')
router.register(r'issues', IssueViewSet, basename='issue')
router.register(r'comment', CommentViewSet, basename='comment')


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
