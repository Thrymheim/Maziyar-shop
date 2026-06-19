from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.core.validators import MinValueValidator , MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length= 20)

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length= 30)
    last_name = models.CharField(max_length= 30)
    phone = models.CharField(max_length= 20)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Product(models.Model):
     name = models.CharField(max_length= 40)
     discription=models.TextField(default='',blank=False ,null=False)
     price = models.DecimalField(default=0 , decimal_places=0 , max_digits=12 )
     category = models.ForeignKey(Category , on_delete=models.CASCADE , default=1)
     picture = models.ImageField(upload_to='upload/product/')
     star = models.IntegerField(default=0 , validators=[MaxValueValidator(5),MinValueValidator(0)])
     is_sale = models.BooleanField(default=False)
     sale_price = models.DecimalField(default=0 , decimal_places=0 , max_digits=12 )

     def __str__(self):
        return self.name

     def get_average_rating(self):
         comments = self.comment_set.all()
         if comments.exists():
             return round(sum(c.rating for c in comments) / comments.count(), 1)
         return self.star

     def get_comments_count(self):
         return self.comment_set.count()


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE )
    customer = models.ForeignKey(Customer , on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=400 ,default='' , blank=True)
    phone = models.CharField(max_length= 20 , blank=True)
    date = models.DateField(default=timezone.now)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.customer} - {self.product.name}'


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.user.username} - {self.product.name} ({self.rating}★)'


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email