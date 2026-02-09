from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('registration',views.UserRegisterView,basename='registration')

urlpatterns = [
    path('',include(router.urls)),
]
