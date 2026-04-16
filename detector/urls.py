from __future__ import annotations

from django.urls import path

from detector import views


app_name = "detector"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("run/", views.run_detection_view, name="run"),
    path("runs/<int:run_id>/", views.run_detail, name="run_detail"),
]
