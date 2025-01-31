from django.urls import path
from .views import (
        ServiceCategoryListView,
        ServiceRequestListCreateView,
        ServiceRequestDetailView,
        admin_service_requests,
        admin_cancel_service_request
    )

urlpatterns = [
    path('categories/', ServiceCategoryListView.as_view(), name='service-category-list'),
    path('', ServiceRequestListCreateView.as_view(), name='service-request-list'),
    path('<int:pk>/', ServiceRequestDetailView.as_view(), name='service-request-detail'),
    path("admin/all-requests/", admin_service_requests, name="admin_service_requests"),
    path("admin/cancel-request/<int:service_id>/", admin_cancel_service_request, name="admin_cancel_service_request"),
]
