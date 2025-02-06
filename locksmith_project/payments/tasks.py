import razorpay
from django.conf import settings
from celery import shared_task
from .models import Transaction
from users.models import User
from celery.schedules import crontab
from celery import Celery

razorpay_client = razorpay.Client(auth=(settings.RAZORPAYX_KEY_ID, settings.RAZORPAYX_KEY_SECRET))

@shared_task
def process_scheduled_payouts():
    """Automatically send payouts to locksmiths for completed transactions"""
    transactions = Transaction.objects.filter(paid_to_locksmith=False)

    for transaction in transactions:
        locksmith = transaction.service_request.locksmith.user  # Locksmith's user object

        # Deduct commission
        commission = transaction.amount * (settings.PLATFORM_COMMISSION_PERCENTAGE / 100)
        payout_amount = transaction.amount - commission

        # Get locksmith's UPI or bank account
        recipient_account = locksmith.upi_id or locksmith.bank_account
        if not recipient_account:
            continue  # Skip payout if no bank/UPI details

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

        # Update transaction status
        transaction.paid_to_locksmith = True
        transaction.razorpay_payout_id = payout["id"]
        transaction.save()
        
celery_app = Celery("locksmith_project")

celery_app.conf.beat_schedule = {
    "process_scheduled_payouts": {
        "task": "payments.tasks.process_scheduled_payouts",
        "schedule": crontab(hour=0, minute=0),  # Runs daily at midnight
    },
}


@shared_task
def process_payouts():
    """Send payments to locksmiths after commission deduction"""
    transactions = Transaction.objects.filter(paid_to_locksmith=False)

    for transaction in transactions:
        locksmith = transaction.service_request.locksmith.user
        commission = transaction.amount * (settings.PLATFORM_COMMISSION_PERCENTAGE / 100)
        payout_amount = transaction.amount - commission

        # Process payout
        payout = razorpay_client.payout.create({
            "account_number": "your-razorpayx-account-number",
            "amount": int(payout_amount * 100),
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

        # Mark transaction as paid
        transaction.paid_to_locksmith = True
        transaction.razorpay_payout_id = payout["id"]
        transaction.save()
