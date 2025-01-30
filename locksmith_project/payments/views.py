from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import generics
from .models import Transaction
from .serializers import TransactionSerializer
import razorpay
from django.conf import settings
from .models import Transaction
from services.models import ServiceRequest
from rest_framework.decorators import api_view, permission_classes

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


# Initialize Razorpay Client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_razorpay_order(request):
    """Create a Razorpay order for a service request"""
    service_id = request.data.get('service_id')

    try:
        service_request = ServiceRequest.objects.get(id=service_id, customer=request.user)

        # Razorpay Order Payload
        print(service_request.price)
        order_amount = int(service_request.price * 100)  # Convert to paisa (INR)
        order_currency = "INR"

        razorpay_order = razorpay_client.order.create({
            "amount": order_amount,
            "currency": order_currency,
            "payment_capture": "1",  # Auto-capture payment
            "notes": {"service_request_id": service_request.id}
        })

        return Response({
            "order_id": razorpay_order["id"],
            "amount": order_amount,
            "currency": order_currency,
            "razorpay_key": settings.RAZORPAY_KEY_ID
        })

    except ServiceRequest.DoesNotExist:
        return Response({"error": "Invalid service request"}, status=400)


@api_view(['POST'])
def razorpay_webhook(request):
    """Handle Razorpay payment success"""
    payload = request.data

    try:
        event = payload.get("event")
        if event == "payment.captured":
            order_id = payload["payload"]["payment"]["entity"]["order_id"]
            amount = payload["payload"]["payment"]["entity"]["amount"] / 100  # Convert from paisa

            # Find service request
            service_request = ServiceRequest.objects.get(id=int(payload["payload"]["payment"]["entity"]["notes"]["service_request_id"]))

            # Create a transaction record
            Transaction.objects.create(
                user=service_request.customer,
                service_request=service_request,
                amount=amount,
                commission=amount * 0.10,  # 10% platform fee
                paid_to_locksmith=False
            )

            # Update service request status
            service_request.status = "completed"
            service_request.save()

        return Response({"status": "success"})
    
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['POST'])
@permission_classes([IsAdminUser])  # Only admin can trigger payouts
def process_payout(request, transaction_id):
    """Send payout to locksmith after commission deduction"""
    try:
        transaction = Transaction.objects.get(id=transaction_id, paid_to_locksmith=False)
        locksmith = transaction.service_request.locksmith.user  # Locksmith's user object

        # Deduct commission
        commission = transaction.amount * (settings.PLATFORM_COMMISSION_PERCENTAGE / 100)
        payout_amount = transaction.amount - commission

        # Get locksmith's UPI or Bank Account details (Assuming stored in user model)
        recipient_account = locksmith.upi_id or locksmith.bank_account

        if not recipient_account:
            return Response({"error": "Locksmith has no payout details"}, status=400)

        # Create Razorpay Payout
        payout = razorpay_client.payout.create({
            "account_number": "your-razorpayx-account-number",
            "amount": int(payout_amount * 100),  # Convert to paisa
            "currency": "INR",
            "mode": "UPI" if locksmith.upi_id else "NEFT",
            "purpose": "payout",
            "fund_account": {
                "account_type": "vpa" if locksmith.upi_id else "bank_account",
                "vpa": {"address": locksmith.upi_id} if locksmith.upi_id else None,
                "bank_account": {
                    "name": locksmith.full_name,
                    "ifsc": locksmith.ifsc_code,
                    "account_number": locksmith.bank_account,
                } if locksmith.bank_account else None,
            },
            "notes": {"service_request_id": transaction.service_request.id}
        })

        # Update transaction with payout details
        transaction.paid_to_locksmith = True
        transaction.razorpay_payout_id = payout["id"]
        transaction.save()

        return Response({"message": "Payout processed successfully", "payout_id": payout["id"]})
    
    except Transaction.DoesNotExist:
        return Response({"error": "Transaction not found"}, status=404)
    
    except Exception as e:
        return Response({"error": str(e)}, status=400)
