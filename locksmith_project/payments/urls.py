from django.urls import path
from .views import TransactionListView, TransactionDetailView
from .views import create_razorpay_order, razorpay_webhook, process_payout

urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction-list'),
    path('<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('create-razorpay-order/', create_razorpay_order, name='create_razorpay_order'),
    path('razorpay-webhook/', razorpay_webhook, name='razorpay_webhook'),
    path('payout/<int:transaction_id>/', process_payout, name='process_payout'),
]
