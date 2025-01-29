from rest_framework import generics
from .models import ServiceRequest, ServiceCategory
from .serializers import ServiceRequestSerializer, ServiceCategorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class ServiceCategoryListView(generics.ListCreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer

class ServiceRequestListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role != 'customer':
            return Response({'error': 'Only customers can request services'}, status=403)
        return super().create(request, *args, **kwargs)

class ServiceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
