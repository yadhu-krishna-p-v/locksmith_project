from django.urls import path
from .views import LocksmithProfileListCreateView, LocksmithProfileDetailView
from .views import (
    approve_locksmith,
    reject_locksmith,
    list_locksmith_services,
    add_locksmith_service,
    remove_locksmith_service,
    update_locksmith_location,
    update_service_price
    )

urlpatterns = [
    path('', LocksmithProfileListCreateView.as_view(), name='locksmith-list'),
    path('<int:pk>/', LocksmithProfileDetailView.as_view(), name='locksmith-detail'),
    path('approve/<int:locksmith_id>/', approve_locksmith, name='approve_locksmith'),
    path("reject/<int:locksmith_id>/", reject_locksmith, name="reject_locksmith"),
    path("services/", list_locksmith_services, name="list_locksmith_services"),
    path("services/add/", add_locksmith_service, name="add_locksmith_service"),
    path("services/remove/<int:service_id>/", remove_locksmith_service, name="remove_locksmith_service"),
    path("update-location/", update_locksmith_location, name="update_locksmith_location"),
    path("services/update-price/<int:service_id>/", update_service_price, name="update_service_price"),
]
