from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from utils.pagination import Paginator

class CommentAPIView(APIView):
    
    def post(self, request, book_pk, *args, **kwargs):
        data = request.data
        serializer = CreateCommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        book = get_object_or_404(Book, id=book_pk)
        reply_to = serializer.validated_data.get('reply_to', None)
        if reply_to:
            reply_to= get_object_or_404(Comment, id=reply_to)
            serializer.validated_data['reply_to'] = reply_to
        serializer.validated_data['user'] = user
        serializer.validated_data['book'] = book
        comment = serializer.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, HTTP_201_CREATED)
    
    def patch(self, request, book_pk, comment_pk, *args, **kwargs):
        data = request.data
        comment = get_object_or_404(Comment, id=comment_pk , book__id = book_pk)
        serializer = UpdateCommentSerializer(data= data, instance=comment)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, HTTP_200_OK)
    
    def delete(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, id=pk)
        comment.delete()
        return Response(HTTP_204_NO_CONTENT)
    
    def _get_object(self, request, book_pk, comment_pk, klass):
        comment = get_object_or_404(klass, id=comment_pk, book__id = book_pk)
        serializer = CommentSerializer(comment)
        return serializer.data
    
    def _get_list(self, request, book_pk, comment_pk, klass):
        limit = request.GET.get('limit', '100')
        page = request.GET.get('page', '1')
        comments = klass.filter(book__id = book_pk)
        paginator = Paginator(
            page_size= limit,
            page= page,
            items= comments
        )
        comments, data = paginator.paginate()
        serializer = ListCommentSerializer(comments, many=True)
        data['items'] = serializer.data
        return data
    
    def get(self, request, book_pk, comment_pk = None, *args, **kwargs):
        klass = Comment.objects.prefetch_related('replies')
        if comment_pk:
            response = self._get_object(request, book_pk, comment_pk, klass)
        else :
            response = self._get_list(request, book_pk, comment_pk, klass)
        return Response(response, HTTP_200_OK)
