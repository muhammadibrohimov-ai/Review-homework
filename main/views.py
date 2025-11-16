from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from django.db.models import Count
from django.shortcuts import get_list_or_404, get_object_or_404

from .models import Categories, Products
from .serializers import CategorySerializer, ProductSerializer

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    
    categories = Categories.objects.annotate(product_count=Count('products')).filter(product_count__gt=0)
    serializer = CategorySerializer(categories, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_all_categories(request):
    
    if request.method == 'GET':
        categories = Categories.objects.annotate(product_count=Count('products')).filter(product_count__gt=0)
        serializer = CategorySerializer(categories, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        data = request.data
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'New category created_successfuly','data':serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def detail_category(request, pk):
    
    def get_object(pk):
        return get_object_or_404(Categories, pk=pk, products__quantity__gte=0)
    
    category = get_object(pk)
    
