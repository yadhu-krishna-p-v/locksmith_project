from rest_framework import generics
from .models import ServiceRequest, ServiceCategory
from .serializers import ServiceRequestSerializer, ServiceCategorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class ServiceCategoryListView(generics.ListCreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer

class ServiceRequestListCreateView(generics.ListCreateAPIView):
    """Customers can create service requests"""
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print(f"Authenticated User: {self.request.user}")  # Debugging
        print(f"User Role: {self.request.user.role}")
        if self.request.user.role != 'customer':
            return Response({'error': 'Only customers can request services'}, status=403)

        serializer.save(customer=self.request.user)

class ServiceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.role != 'locksmith':
            return Response({'error': 'Only locksmiths can accept or reject services'}, status=403)

        return super().update(request, *args, **kwargs)
