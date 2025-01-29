from django.urls import path
from .views import ServiceCategoryListView, ServiceRequestListCreateView, ServiceRequestDetailView

urlpatterns = [
    path('categories/', ServiceCategoryListView.as_view(), name='service-category-list'),
    path('', ServiceRequestListCreateView.as_view(), name='service-request-list'),
    path('<int:pk>/', ServiceRequestDetailView.as_view(), name='service-request-detail'),
]
