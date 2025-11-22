from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from django.shortcuts import get_object_or_404


from a_books.serializers.book_serializers import *
from a_books.serializers.category_serializers import *

class CategoryView(APIView):
    
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            category = get_object_or_404(Category, id=pk)
            serializer = CategorySerializer(category)
        else:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CreateCategorySerializer(data=data)
        serializer.is_valid(raise_exception = True)
        category= None
        if serializer.check_category_existence():
            category = Category.objects.get(name__iexact= serializer.validated_data['name'])
        if not category:
            category = serializer.save()
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=HTTP_201_CREATED)
    
    def delete(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, id=pk)
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk, *args, **kwargs):
        data = request.data
        category = get_object_or_404(Category, id=pk)
        serializer = UpdateCategorySerializer(data=data, instance=category)
        serializer.is_valid(raise_exception=True)
        category= serializer.save()
        serializer = CategorySerializer(category)
        return Response(serializer.data,status=HTTP_200_OK)