from account.api import views

from rest_framework.routers import DefaultRouter


app_name = 'api-user'

router = DefaultRouter()
router.register('avatars', views.AvatarAPIViewSet, basename='avatar')
router.register('users', views.UserAPIViewSet, basename='user')

urlpatterns = router.urls
