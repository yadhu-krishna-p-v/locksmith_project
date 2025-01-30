from django.urls import path
from .views import LocksmithProfileListCreateView, LocksmithProfileDetailView
from .views import approve_locksmith

urlpatterns = [
    path('', LocksmithProfileListCreateView.as_view(), name='locksmith-list'),
    path('<int:pk>/', LocksmithProfileDetailView.as_view(), name='locksmith-detail'),
    path('approve/<int:locksmith_id>/', approve_locksmith, name='approve_locksmith'),
]
