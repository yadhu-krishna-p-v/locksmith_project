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
