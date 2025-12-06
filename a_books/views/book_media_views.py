from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from django.shortcuts import get_object_or_404
from a_books.models.book_media import *

from a_books.serializers.book_media_serializer import BookMediaSerializers
from a_users.permissions import IsAdmin
from utils.cloudinary import Cloudinary, CloudinaryResourceType
from a_books.models.book import Book

class BookMediaAPIView(APIView):
    permission_classes = [IsAdmin
                          ]
    def delete(self, request, public_id, type, *args, **kwargs):
        try:
            uploader = Cloudinary.get_instance()
            resource_type = CloudinaryResourceType[type.upper()]
            
            # check public id
            if not BookMedia.objects.filter(public_id = public_id).exists():
                return Response({'public_id' : 'public_id is not valid'},HTTP_400_BAD_REQUEST)
            
            # delete file
            is_deleted, msg = uploader.delete_file(public_id = public_id, resource_type = resource_type)
            
            if is_deleted:
                # clean DB
                media = BookMedia.objects.filter(public_id = public_id)
                media.delete()
                return Response(status=HTTP_204_NO_CONTENT)
            
            return Response({'detail' : msg},HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail' : 'Something went wrong try again later'},HTTP_400_BAD_REQUEST)
            
    def post(self, request, pk, type, *args, **kwargs):
        
        # get file from request
        file = request.FILES.get('file')
        
        if not file:
            return Response({'detail' : 'No file uploaded'},HTTP_400_BAD_REQUEST)
        
        book = get_object_or_404(Book, id=pk)
        
        try:
            uploader = Cloudinary.get_instance()
            resource_type = CloudinaryResourceType[type.upper()]
            
            # upload file
            is_uploaded, data = uploader.upload_file(
                file = file,
                resource_type = resource_type,
                folder = 'book_media')
            
            if not is_uploaded:
                return Response({'detail' : data}, HTTP_400_BAD_REQUEST)
            
            serializer = BookMediaSerializers(data= data)
            if serializer.is_valid():
                serializer.save(book= book)
            else:
                return Response({'detail' : 'Something went wrong try again later'},HTTP_400_BAD_REQUEST)
            return Response(serializer.data, HTTP_200_OK) 
        except Exception as e:
            print(f'Exception : {e}')
            return Response({'detail' : 'Something went wrong try again later'},HTTP_400_BAD_REQUEST)
            
        
        