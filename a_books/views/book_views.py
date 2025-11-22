from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import *
from django.shortcuts import get_object_or_404
from django.db.models import Q
from a_books.serializers.book_serializers import *
from a_books.serializers.category_serializers import *
      
class BookView(APIView):
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CreateBookSerializer(data=data)
        serializer.is_valid(raise_exception = True)
        book = serializer.save()
        serializer = BookSerializer(book)
        return Response(serializer.data, status=HTTP_201_CREATED)
        
    def patch(self, request, pk, *args, **kwargs):
        data = request.data
        book = get_object_or_404(Book, id=pk)
        serializer = UpdateBookSerializer(instance=book, data=data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save() 
        serializer = BookSerializer(book)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def delete(self, request, pk, *args, **kwargs):
        book = get_object_or_404(Book, id=pk)
        book.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            book = get_object_or_404(Book, id=pk)
            serializer = BookSerializer(book)
        else:
            books = Book.objects.all().prefetch_related('authors', 'categories')
            serializer = BookSerializer(books, many=True)
        return Response(serializer.data,status=HTTP_200_OK)
      
class BookCategoryView(APIView):
    
    def patch(self, request, pk, *args, **kwargs): 
        data = request.data 
        book = get_object_or_404(Book, id=pk)
        serializer = UpdateBookCategoriesSerializer(instance=book, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.add_categories()
        return Response(serializer.data, HTTP_200_OK)
    
    def delete(self, request, pk, *args, **kwargs): 
        data = request.data 
        book = get_object_or_404(Book, id=pk)
        serializer = UpdateBookCategoriesSerializer(instance=book, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.remove_categories()
        return Response(serializer.data,HTTP_200_OK)

class BookAuthorsView(APIView):
    
    def patch(self, request, pk, *args, **kwargs): 
        data = request.data 
        book = get_object_or_404(Book, id=pk)
        serializer = UpdateBookAuthorSerializer(instance=book, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.add_authors()
        return Response(serializer.data,HTTP_200_OK)
    
    def delete(self, request, pk, *args, **kwargs): 
        data = request.data 
        book = get_object_or_404(Book, id=pk)
        serializer = UpdateBookAuthorSerializer(instance=book, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.remove_authors()
        return Response(serializer.data,HTTP_200_OK)

class BookSearchView(APIView):
    
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q','').strip()
        books = Book.objects.search(q)
        print(books)
        serializer= BookSerializer(books, many=True)
        return Response(serializer.data, HTTP_200_OK)
    