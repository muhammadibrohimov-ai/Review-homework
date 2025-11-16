from django.shortcuts import render
from rest_framework import permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import Count
from django.shortcuts import get_list_or_404, get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from .models import Categories, Products
from .serializers import CategorySerializer, ProductSerializer

# Create your views here.

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def home(request):
    
    categories = Categories.objects.annotate(product_count=Count('products')).filter(product_count__gt=0)
    serializer = CategorySerializer(categories, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
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
@permission_classes([permissions.IsAuthenticated])
def detail_category(request, pk):
    
    def get_object(pk):
        return get_object_or_404(Categories, pk=pk)
    
    def update(data, pk, partial=False):
        obj = get_object(pk)
        serializer = CategorySerializer(obj, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':f'The category with id {pk} has been updated!', "data":serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    
    if request.method == 'GET':
        obj = get_object(pk)
        obj = CategorySerializer(obj)
        return Response(obj.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        return update(request.data, pk, partial=False) 
    
    if request.method == 'PATCH':
        return update(request.data, pk, partial=True)
    
    if request.method == 'DELETE':
        obj = get_object(pk)
        obj.delete()
        return Response({'message':f'The category with id {pk} has been deleted!'}, status=status.HTTP_202_ACCEPTED)
    

@permission_classes([permissions.IsAuthenticated])
class ProductView(APIView):
    
    def get_objects(self):
        return get_list_or_404(Products)
    
    def get(self, request):
        objs = self.get_objects()
        serializer = ProductSerializer(objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'New product has been created','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


class ProductDetail(RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'quantity']
    search_fields = ['name', 'category__name', 'price', 'quantity']


class 