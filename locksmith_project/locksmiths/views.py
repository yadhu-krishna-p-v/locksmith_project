from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from .models import LocksmithProfile
from .serializers import LocksmithProfileSerializer

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
