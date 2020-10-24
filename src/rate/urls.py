from django.urls import path

from rate import views

app_name = 'rate'

urlpatterns = [
    path('list/', views.RateListView.as_view(), name='list'),
    path('list/csv/', views.CSVView.as_view(), name='list-csv'),
    path('list/xlsx/', views.XLSXView.as_view(), name='list-xlsx'),
    path('contact-us/create/', views.CreateContactUsView.as_view(), name='contact-us-create'),
    path('feedback/', views.CreateFeedbackView.as_view(), name='feedback'),
    path('list/latest/', views.LatestRates.as_view(), name='list-latest'),

]
