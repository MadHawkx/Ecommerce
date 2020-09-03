from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from supplier.models import Supplier_Account
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ManyToManyField(Category, blank=False)
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200)
    description = models.CharField(max_length=250)
    discount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    staffRecommended = models.BooleanField(default=False)
    supplier = models.ForeignKey(Supplier_Account, on_delete=models.CASCADE)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    @property
    def is_staffRecommended(self):
        return self.staffRecommended


class Size(models.Model):
    size = models.CharField(max_length=50)

    def __str__(self):
        return self.size


class Color(models.Model):
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.color


class Product_Size_Color(models.Model):
    STATUS_CHOICES = (
        ('default', 'DEFAULT'),
        ('updated', 'UPDATED'),
        ('deleted', 'DELETED'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField()
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='default')

    class Meta:
        unique_together = (('product', 'size', 'color'))

    def __str__(self):
        return self.product.name


class Product_Images(models.Model):
    product_size_color = models.ForeignKey(
        Product_Size_Color, on_delete=models.CASCADE)
    Image = models.ImageField(upload_to='product/images')


class Product_History(models.Model):
    product_size_color = models.ForeignKey(
        Product_Size_Color, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField()
    datetime = models.DateTimeField()

    def __str__(self):
        return self.product_size_color.product.name
