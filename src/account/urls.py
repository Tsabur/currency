from account import views

from django.urls import path

app_name = 'account'

urlpatterns = [
    # path('my-profile/<int:pk>/', views.MyProfile.as_view(), name='my_profile'),
    path('my-profile/', views.MyProfile.as_view(), name='my_profile'),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('avatar/create', views.CreateUserAvatar.as_view(), name='avatar-create'),
    path('avatars/list/', views.Avatars.as_view(), name='avatars'),
    path('activate/<str:username>', views.ActivateUser.as_view(), name='activate'),

]
