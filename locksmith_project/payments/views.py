from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import generics
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionListView(generics.ListCreateAPIView):
    """Customers can make payments"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role != 'customer':
            return Response({'error': 'Only customers can make payments'}, status=403)
        return super().create(request, *args, **kwargs)

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser]
