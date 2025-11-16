from rest_framework import serializers
from .models import Categories, Products

# Create your serializers here.

class ProductSerializer(serializers.ModelSerializer):
    
    category = serializers.PrimaryKeyRelatedField(
        queryset = Categories.objects.all()
    )
    
    class Meta:
        model = Products
        fields = ['id', 'name', 'desc', 'image', 'quantity', 'category', 'updated_at', 'created_at']
        read_only_fields = ['id', 'updated_at', 'created_at',]
        
    def validate(self, attrs):
        name = attrs.get('name', '').lower().strip()
        
        if not name:
            raise serializers.ValidationError('The name field can\'t be empty!' )

        existing = Products.objects.filter(name__iexact = name)
            
        if self.instance:
            existing = existing.exclude(id=self.instance.id)

        if existing.exists():
            raise serializers.ValidationError("The product with this name already exists!")

        return attrs


class CategorySerializer(serializers.ModelSerializer):
    
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Categories
        fields = ['id', 'name', 'created_at', 'updated_at', 'products']
        read_only_fields = ['id', 'created_at', 'updated_at', 'products']
        
    def validate(self, attrs):
        name = attrs.get('name', '').lower().strip()
        
        if not name:
            raise serializers.ValidationError('The name field can\'t be empty!' )

        existing = Categories.objects.filter(name__iexact = name)
            
        if self.instance:
            existing = existing.exclude(id=self.instance.id)

        if existing.exists():
            raise serializers.ValidationError("The category with this name already exists!")

        return attrs
    

    
