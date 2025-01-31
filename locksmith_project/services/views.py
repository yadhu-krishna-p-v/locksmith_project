from rest_framework import generics
from .models import ServiceRequest, ServiceCategory
from .serializers import ServiceRequestSerializer, ServiceCategorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes

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
    

@api_view(["GET"])
@permission_classes([IsAdminUser])  # Only admins can access
def admin_service_requests(request):
    """Retrieve all service requests for admin"""
    service_requests = ServiceRequest.objects.all()
    serializer = ServiceRequestSerializer(service_requests, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAdminUser])  # Only admins can cancel
def admin_cancel_service_request(request, service_id):
    """Admin cancels a service request"""
    try:
        service_request = ServiceRequest.objects.get(id=service_id)

        if service_request.status in ["completed", "cancelled", "failed"]:
            return Response({"error": "This request cannot be cancelled"}, status=400)

        service_request.status = "cancelled"
        service_request.save()
        return Response({"message": "Service request cancelled successfully"})
    
    except ServiceRequest.DoesNotExist:
        return Response({"error": "Service request not found"}, status=404)
