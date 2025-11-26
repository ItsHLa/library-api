from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from django.shortcuts import get_object_or_404
from a_books.serializers.book_serializers import *
from a_books.serializers.category_serializers import *
from a_users.permissions import IsAdmin
from utils.pagination import Paginator
from a_comments.models import Comment
from django.db.models import Prefetch

class BookView(APIView):
    permission_classes=[IsAdmin]
    
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
    
    def _get_object(self, request, pk):
        # reverse ForeignKey
        book = Book.objects.prefetch_related( 
            Prefetch( ## get comments
                'book_comments',
                queryset = Comment.objects.filter(reply__isnull=True).select_related('user').prefetch_related(
                    Prefetch('replies', ## get_replies
                             queryset= Comment.objects.select_related('user'))
                )
            )
        ).get(id=pk)
        
        if not book:
            return {'detail': 'No Book matches the given query.'}, HTTP_404_NOT_FOUND
        serializer = BookSerializer(book)
        return serializer.data , HTTP_200_OK
    
    def _get_list(self, request, pk=None, *args, **kwargs):
        q = request.GET.get('q', None)
        categories = request.GET.getlist('category','')
        authors = request.GET.getlist('author','')
        c_ids = request.GET.getlist('c_id','')
        a_ids = request.GET.getlist('a_id','')
        page = request.GET.get('page','1') 
        limit = request.GET.get('limit','20')
        
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
        response = {}
        if page and limit:
            paginator = Paginator(
                    page=page,
                    page_size=limit,
                    items=books)
            books, data = paginator.paginate()
            response = data
        serializer = BookListSerializer(books, many=True)
        response['items'] = serializer.data
        return response , HTTP_200_OK
        
    def get(self, request, pk=None, *args, **kwargs):
        response = {}
        status = None
        if pk:
            response, status = self._get_object(request, pk)
        else:
            response, status = self._get_list(request, pk)
        return Response(response,status=status)
        
class BookCategoryView(APIView):
    
    def patch(self, request, pk, *args, **kwargs): 
        data = request.data 
        book = get_object_or_404(Book, id=pk)
        serializer = UpdateBookCategoriesSerializer(instance=book, data=data)
        categories = get_list_or_404(Category, pk__in= serializer.validated_data['categories'])
        serializer.validated_data['categories'] = categories
        serializer.is_valid(raise_exception=True)
        serializer.add_categories()
        return Response(serializer.data, HTTP_200_OK)
    
    def delete(self, request, pk, *args, **kwargs): 
        data = request.data 
        book = get_object_or_404(Book, id=pk)
        serializer = UpdateBookCategoriesSerializer(instance=book, data=data)
        categories = get_list_or_404(Category, pk__in= serializer.validated_data['categories'])
        serializer.validated_data['categories'] = categories
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