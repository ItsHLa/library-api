from rest_framework import serializers

from a_books.models.book_media import BookMedia

class UpdateBookMediaSerializers(serializers.Serializer):
    public_id = serializers.CharField(max_length=500, required=False)
    resource_type = serializers.CharField(max_length=100, required=False)
    bytes = serializers.IntegerField(required=False)
    secure_url = serializers.URLField(required=False)
    display_name = serializers.CharField(max_length=100, required=False)
    
    def update(self, instance, validated_data):
        return BookMedia.objects.update(**validated_data)

class BookMediaSerializers(serializers.Serializer):
    public_id = serializers.CharField(max_length=500)
    resource_type = serializers.CharField(max_length=100)
    bytes = serializers.IntegerField()
    secure_url = serializers.URLField()
    display_name = serializers.CharField(max_length=100)
    
    def create(self, validated_data):
        print(validated_data)
        return BookMedia.objects.create(**validated_data)