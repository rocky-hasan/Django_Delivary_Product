
from django.urls import path
from .views import Index,About,Order,OrderConfirmation,OrderPayConfirmation


urlpatterns = [
    path('',Index.as_view(),name='home'),
    path('about/',About.as_view(),name='about'),
    path('order/',Order.as_view(),name='order'),
    path('orderconfirm/<int:pk>/',OrderConfirmation.as_view(),name='orderconfirm'),
    path('paymentconfirm/',OrderPayConfirmation.as_view(),name='paymentconfirm'),
]
