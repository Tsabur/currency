from rate.api import views

from rest_framework.routers import DefaultRouter

app_name = 'api-rate'

router = DefaultRouter()
router.register('rates', views.RateAPIViewSet, basename='rate')

urlpatterns = router.urls

# path('api/rates/', views.RateListAPIView.as_view(), name='api-rates'),
# path('api/rates/<int:pk>/', views.RateAPIView.as_view(), name='api-rate'),
