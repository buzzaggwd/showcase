from django.urls import path

from . import views

urlpatterns = [
    path("api/services/", views.GetServiceInfoView.as_view()),
    path("api/services/data/", views.GetServiceDataInfoView.as_view()),
]