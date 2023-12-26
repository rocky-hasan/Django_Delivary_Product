
from django.urls import path
from .views import Index,About,Order


urlpatterns = [
    path('',Index.as_view(),name='home'),
    path('about/',About.as_view(),name='about'),
    path('order/',Order.as_view(),name='order'),
]
