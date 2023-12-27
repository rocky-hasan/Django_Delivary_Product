from django.shortcuts import render,redirect
from django.views import View
from .models import Category,MenuItem,OrderModel
from django.core.mail import send_mail
# Create your views here.

class Index(View):
    def get(self,request,*args,**kwargs):
        return render(request, 'index.html')

class About(View):
    def get(self,request,*args,**kwargs):
        return render(request, 'about.html')
    

class Order(View):

    def get(self,request,*args,**kwargs):

        appetizers=MenuItem.objects.filter(category__name__contains='Appetizer')
        drinks=MenuItem.objects.filter(category__name__contains='Drink')
        desert=MenuItem.objects.filter(category__name__contains='Desert')
        first_food=MenuItem.objects.filter(category__name__contains='First_Food')
        context={
            'appetizers':appetizers,
            'drinks':drinks,
            'deserts':desert,
            'first_food':first_food,
        }
        return render(request, 'order.html',context)
    
    def post(self, request, *args, **kwargs):
        name=request.POST.get('name')
        email=request.POST.get('email')
        street=request.POST.get('street')
        state=request.POST.get('state')
        city=request.POST.get('city')
        zipcode=request.POST.get('zipcode')
        
        order_items = {
            'items': []  #empty dictionary
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            state=state,
            city=city,
            zipcode=zipcode,
        )
        order.items.add(*item_ids)
        # Here email confirmation work 
        body=('Order deliver soon\n'
              f'total amount: {price}\n'
              'thank you for order')

        send_mail(
            'Thank you for your order',
            body,
            'rockyhasan@gmail.com', # from email
            [email],  #  who received
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('orderconfirm',pk=order.pk)

class OrderConfirmation(View):
    def get(self,request,pk,*args,**kwargs):
        order=OrderModel.objects.get(pk=pk)
        context={
            'pk': order.pk,
            'items': order.items,
            'price': order.price

        }
        return render(request, 'order_confirmation.html', context)
    def post(self,request,pk,*args,**kwargs):
        print(request.body)

class OrderPayConfirmation(View):
    def get(self,request,pk,*args,**kwargs):
        return render(request,'Order_pay_confirmation.html')
