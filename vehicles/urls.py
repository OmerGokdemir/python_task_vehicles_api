from django.urls import path
from .views import VehicleAPIView

urlpatterns = [
    path('upload/', VehicleAPIView.as_view(), name='upload-vehicle'),
]
