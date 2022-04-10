from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome_page),
    path('news/', views.MainPageView.as_view(), name='main'),
    path('news/<int:link>', views.SinglePageView.as_view()),
    path('new/create/', views.CreateNewsView.as_view(), name='create'),

]