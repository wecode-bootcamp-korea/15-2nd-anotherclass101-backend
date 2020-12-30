from django.db import models


class ProductTypes(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'product_types'
    def __str__(self):
        return self.name


class Goods(models.Model):
    description   = models.CharField(max_length=150)
    delivery_info = models.CharField(max_length=150)

    class Meta:
        db_table = 'goods'


class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'
    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name     = models.CharField(max_length=45)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'
    def __str__(self):
        return self.name


class CourseLevel(models.Model):
    name = models.CharField(max_length=15)

    class Meta:
        db_table = 'course_levels'
    def __str__(self):
        return self.name


class Product(models.Model):
    name          = models.CharField(max_length=45)
    price         = models.DecimalField(decimal_places=2,max_digits=20)
    sub_category  = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    product_type  = models.ForeignKey(ProductTypes, on_delete=models.CASCADE)
    refund_policy = models.CharField(max_length=200, null=True)
    liker         = models.ManyToManyField('user.User', through='ProductLike', related_name='liked_products')

    class Meta:
        db_table = 'products'
    def __str__(self):
        return self.name


class ProductLike(models.Model):
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_likes'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img_url = models.URLField()

    class Meta:
        db_table = 'product_images'


class CourseStatus(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'course_status'
    def __str__(self):
        return self.name


class Course(models.Model):
    curriculum          = models.CharField(max_length=45)
    class_status        = models.ForeignKey(CourseStatus, on_delete=models.CASCADE)
    kit_description     = models.CharField(max_length=200, null=True)
    benefit             = models.CharField(max_length=100)
    creator             = models.ForeignKey('user.Creator', on_delete=models.CASCADE)
    creator_description = models.CharField(max_length=200)
    product             = models.ForeignKey(Product, on_delete=models.CASCADE)
    level               = models.ForeignKey(CourseLevel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'courses'
    def __str__(self):
        return self.curriculum


class Like(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'likes'


class CourseReview(models.Model):
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    body       = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course     = models.ForeignKey(Course, on_delete=models.CASCADE)
    like       = models.ForeignKey(Like, on_delete=models.CASCADE)

    class Meta:
        db_table = 'course_reviews'


class CourseFaq(models.Model):
    question = models.CharField(max_length=150)
    answer   = models.CharField(max_length=500)
    course   = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        db_table = 'course_faqs'


class CourseMaterial(models.Model):
    course  = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    name    = models.CharField(max_length=45, null=True)
    price   = models.DecimalField(decimal_places=2,max_digits=20)
    maximum = models.IntegerField(null=True)

    class Meta:
        db_table = 'course_materials'
    def __str__(self):
        return self.name


class GoodsReview(models.Model):
    user        = models.ForeignKey('user.User', on_delete=models.CASCADE)
    goods       = models.ForeignKey(Goods, on_delete=models.CASCADE)
    body        = models.CharField(max_length=100)
    rating      = models.FloatField()
    img_url     = models.URLField(null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goods_reviews'
