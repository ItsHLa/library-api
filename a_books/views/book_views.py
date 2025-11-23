from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from django.shortcuts import get_object_or_404
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
        q = request.GET.get('q', None)
        categories = request.GET.getlist('category','')
        authors = request.GET.getlist('author','')
        c_ids = request.GET.getlist('c_id','')
        a_ids = request.GET.getlist('a_id','')
        
        if pk:
            ## book Detail
            book = get_object_or_404(Book, id=pk)
            serializer = BookSerializer(book)
        else:
            books = Book.objects.all().prefetch_related('authors', 'categories')
            
            ## searching for books
            if q:
                books = books.search(q)
                
            ## filter books
            if c_ids:
                c_ids= list(map(int, c_ids))
                books = books.filter_by_category_ids(c_ids)
            if a_ids:
                a_ids= list(map(int, a_ids))
                books = books.filter_by_author_ids(a_ids)
            if categories:
                books = books.filter_by_category_names(categories)
            if authors:
                books = books.filter_by_author_names(authors)
                
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