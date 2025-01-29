from django.urls import path
from .views import LocksmithProfileListCreateView, LocksmithProfileDetailView

urlpatterns = [
    path('', LocksmithProfileListCreateView.as_view(), name='locksmith-list'),
    path('<int:pk>/', LocksmithProfileDetailView.as_view(), name='locksmith-detail'),
]
