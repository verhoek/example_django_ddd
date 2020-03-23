from django.urls import path

from app.views import CreateRootEntityView, UpdateRootEntityView

urlpatterns = [
    path('', CreateRootEntityView.as_view()),
    path('<int:pk>', UpdateRootEntityView.as_view()),
]
