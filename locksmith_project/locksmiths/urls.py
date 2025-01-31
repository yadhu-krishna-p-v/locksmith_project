from django.urls import path
from .views import LocksmithProfileListCreateView, LocksmithProfileDetailView
from .views import approve_locksmith, reject_locksmith

urlpatterns = [
    path('', LocksmithProfileListCreateView.as_view(), name='locksmith-list'),
    path('<int:pk>/', LocksmithProfileDetailView.as_view(), name='locksmith-detail'),
    path('approve/<int:locksmith_id>/', approve_locksmith, name='approve_locksmith'),
    path("reject/<int:locksmith_id>/", reject_locksmith, name="reject_locksmith"),
]
