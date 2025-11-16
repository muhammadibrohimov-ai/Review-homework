from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=150)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    


class Products(models.Model):
    name = models.CharField(max_length=150)
    desc = models.TextField()
    image = models.ImageField(upload_to='products')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    category = models.ForeignKey('Categories', related_name='products', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)      
    
    def __str__(self):
        return self.name 
