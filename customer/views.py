from django.shortcuts import render,redirect
from django.views import View
from .models import Category,MenuItem,OrderModel
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
            'desert':desert,
            'first_food':first_food,
        }
        return render(request, 'order.html',context)

    def post(self,request,*args,**kwargs):
        order_items={
            'items':[]
        }
        items=request.POST.getlist('items[]')
        for item in items:
            menu_item=MenuItem.objects.get(pk=int(item))
            item_data={
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price,
            }
            order_items['items'].append(item_data)
            price=0
            item_ids=[]
            for item in order_items['items']:
                price +=item['price']
                item_ids.append(item['id'])
            
            order=OrderModel.objects.create(price=price)
            order.items.add(*item_data)
            context={
                'items':order_items['items'],
                'price':price
            }
            return render(request, 'order_confirm.html',context)
