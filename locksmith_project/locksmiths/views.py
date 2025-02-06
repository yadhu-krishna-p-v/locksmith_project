from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from .models import LocksmithProfile, LocksmithService
from .serializers import LocksmithProfileSerializer, LocksmithServiceSerializer

class LocksmithProfileListCreateView(generics.ListCreateAPIView):
    queryset = LocksmithProfile.objects.all()
    serializer_class = LocksmithProfileSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role != 'locksmith':
            return Response({'error': 'Only locksmiths can create profiles'}, status=403)
        return super().create(request, *args, **kwargs)

class LocksmithProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LocksmithProfile.objects.all()
    serializer_class = LocksmithProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        locksmith = self.get_object()
        if not locksmith.approved:
            return Response({'error': 'Your profile is pending approval'}, status=403)
        return super().get(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([IsAdminUser])  # Only Admins can approve
def approve_locksmith(request, locksmith_id):
    try:
        locksmith = LocksmithProfile.objects.get(id=locksmith_id)
        locksmith.approved = True
        locksmith.save()
        return Response({'message': 'Locksmith approved successfully'})
    except LocksmithProfile.DoesNotExist:
        return Response({'error': 'Locksmith not found'}, status=404)


@api_view(["POST"])
@permission_classes([IsAdminUser])  # Only admins can reject
def reject_locksmith(request, locksmith_id):
    """Admin rejects a locksmith (deletes profile)"""
    try:
        locksmith = LocksmithProfile.objects.get(id=locksmith_id)
        locksmith.delete()
        return Response({"message": "Locksmith rejected and profile deleted"})
    except LocksmithProfile.DoesNotExist:
        return Response({"error": "Locksmith not found"}, status=404)
    
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_locksmith_services(request):
    """List services offered by the authenticated locksmith"""
    locksmith_services = LocksmithService.objects.filter(locksmith=request.user.locksmithprofile)
    serializer = LocksmithServiceSerializer(locksmith_services, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_locksmith_service(request):
    """Locksmith adds a new service"""
    request.data["locksmith"] = request.user.locksmithprofile.id  # Assign current locksmith
    serializer = LocksmithServiceSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_locksmith_service(request, service_id):
    """Locksmith removes a service"""
    try:
        service = LocksmithService.objects.get(id=service_id, locksmith=request.user.locksmithprofile)
        service.delete()
        return Response({"message": "Service removed successfully"})
    except LocksmithService.DoesNotExist:
        return Response({"error": "Service not found"}, status=404)
    

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_locksmith_location(request):
    """Locksmith updates their service area"""
    locksmith = request.user.locksmithprofile
    serializer = LocksmithProfileSerializer(locksmith, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_service_price(request, service_id):
    """Allow locksmiths to update their service pricing"""
    try:
        service = LocksmithService.objects.get(id=service_id, locksmith=request.user.locksmithprofile)
        new_price = request.data.get("price")

        if not new_price or float(new_price) <= 0:
            return Response({"error": "Invalid price"}, status=400)

        service.price = new_price
        service.save()
        return Response({"message": "Service price updated successfully", "new_price": service.price})

    except LocksmithService.DoesNotExist:
        return Response({"error": "Service not found"}, status=404)
