from django.urls import path
from .views import DeveloperCreateView, DeveloperListView, DeveloperDetailView, DeveloperDeleteView

urlpatterns = [
    path('create/', DeveloperCreateView.as_view(), name='developer-create'),
    path('list/', DeveloperListView.as_view(), name='developer-list'),
    path('<int:pk>/', DeveloperDetailView.as_view(), name='developer-detail'),
    path('delete/<int:pk>/', DeveloperDeleteView.as_view(), name='developer-delete'),
]
