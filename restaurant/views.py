from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.shortcuts import render
from datetime import datetime
from customer.models import OrderModel  # Import your OrderModel

class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        today = datetime.today()
        orders = OrderModel.objects.filter(
            created_at__year=today.year,
            created_at__month=today.month,
            created_at__day=today.day
        )
        unshipped=[]
        total_revenue = 0
        for order in orders:
            total_revenue += order.price
            if not order.is_shipped:
                unshipped.append(order)

        context = {
            'orders': unshipped,
            'total_revenue': total_revenue,
            'total_order': len(orders)
        }
        return render(request, 'dashboard.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()

class OrderDetails(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self,request,pk,*args,**kwargs):
        order=OrderModel.objects.get(pk=pk)
        context={
            'order':order
        }
        return render(request, 'order_details.html',context)
    
    def post(self,request,pk,*args,**kwargs):
        order=OrderModel.objects.get(pk=pk)
        order.is_shipped=True
        order.save()
        context={
            'order':order
        }
        return render(request, 'order_details.html',context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()