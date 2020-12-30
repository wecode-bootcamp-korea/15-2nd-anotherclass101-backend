from django.db import models
from product.models import Product,Category
class Platform(models.Model):
    name = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'platforms'
    def __str__(self):
        return self.name


class UserGrade(models.Model):
    name        = models.CharField(max_length=20)
    description = models.CharField(max_length=150)
    
    class Meta:
        db_table = 'user_grades'
    def __str__(self):
        return self.name


class User(models.Model):
    name          = models.CharField(max_length=20)
    email         = models.CharField(max_length=50)
    password      = models.CharField(max_length=150,null=True)
    nickname      = models.CharField(max_length=20, null=True)
    profile_image = models.URLField(default=
    "https://image.ohou.se/i/bucketplace-v2-development/uploads/default_images/avatar.png?gif=1&w=144&h=144&c=c&webp=1", null=True)
    grade         = models.ForeignKey(UserGrade, on_delete=models.CASCADE, null=True, default=1)
    platform      = models.ForeignKey(Platform, on_delete=models.CASCADE, null=True)
    number        = models.CharField(max_length=11, null=True, unique=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
    def __str__(self):
        return self.name


class PhoneVerification(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone = models.CharField(unique=True, max_length=11)
    code  = models.CharField(max_length=6)
    
    class Meta:
        db_table = 'phone_verifications'


class ApplyPath(models.Model):
    reason          = models.CharField(max_length=20)
    specific_reason = models.CharField(max_length=150, null=True)
    recommender     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'apply_paths'


class Creator(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    apply_path  = models.ForeignKey(ApplyPath, on_delete=models.CASCADE)
    information = models.CharField(max_length=150)
    
    class Meta:
        db_table = 'creators'


class RecentView(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    product     =  models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'recent_views'


class Order(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    product       = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at    = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'orders'


class Point(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    change      = models.IntegerField()
    description = models.CharField(max_length=40)
    created_at  = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'points'


class Coupon(models.Model):
    code           = models.CharField(max_length=40)
    start_date     = models.DateTimeField()
    expiry_date    = models.DateTimeField()
    is_used        = models.BooleanField(default=False)
    category       = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    discount_price = models.IntegerField()
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    product        =  models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'coupons'
