from django.db import models

# Create your models here.
class MenuItem(models.Model):
    name=models.CharField(max_length=50)
    desc=models.TextField()
    image=models.ImageField(upload_to='menu_image/')
    price=models.DecimalField(max_digits=5, decimal_places=2)
    category=models.ManyToManyField('Category', related_name='item')

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name

class OrderModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    price=models.DecimalField(max_digits=7, decimal_places=2)
    items=models.ManyToManyField('MenuItem', related_name='order',blank=True)

    def __str__(self):
        return f'Order: {self.created_at}'
