from uuid import uuid4
import cloudinary
import cloudinary.uploader as uploader
import cloudinary.api as api
from enum import Enum
from django.conf import settings


class CloudinaryResourceType(Enum):
    IMAGE = 'image'
    PDF = 'raw'

class Cloudinary:
    
    _instance = None
    
    def set_resource_type(self, resource_type):
        if isinstance(resource_type, CloudinaryResourceType):
            return resource_type.value
        return resource_type
    
    def __init__(self, cloud_name, api_key, api_secret) -> None:
        self._instance = cloudinary.config(
            cloud_name = cloud_name,
            api_key = api_key,
            api_secret = api_secret,
            secure = True)
        self.cloud_name = cloud_name
        self.api_key = api_key
        self.api_secret = api_secret
 
    # singleton
    @classmethod
    def get_instance(cls):
        if not cls._instance:
            print('NEW INSTANCE')
            cloud_name = getattr(settings, 'CLOUD_NAME', None)
            api_key = getattr(settings, 'CLOUD_API_KEY', None)
            api_secret = getattr(settings, 'CLOUD_API_SECRET', None)
            cls._instance = cls(cloud_name, api_key, api_secret)
        return cls._instance
    
    def delete_file(self, public_id= None, resource_type= CloudinaryResourceType.IMAGE):
        
        # get resource_type depending on type
        resource_type = self.set_resource_type(resource_type)
        print(resource_type)
        
        try:
            result = uploader.destroy(
                public_id = f'book_media/{public_id}',
                resource_type = resource_type)
            print(result)
            if result.get('result') == 'ok':
                return True, result.get('result')
            else:
                return False, result.get('result')
        except Exception as e:
            print(f"Exception: {e}")
            return False, str(e)
    
    def get_file(self, public_id= None, resource_type= CloudinaryResourceType.IMAGE ):
        
        # get resource_type depending on type
        resource_type = self.set_resource_type(resource_type)
        print(resource_type)
        
        try:
            result = api.resource(public_id=public_id, resource_type=resource_type)
            return result
        except Exception as e:
            print(f"Exception: {e}")
            return None
    
    def upload_file(self, file, folder='image', resource_type = CloudinaryResourceType.IMAGE):
        
        # get resource_type depending on type
        resource_type = self.set_resource_type(resource_type)
        print(resource_type)
        
        try:
            result = uploader.upload(
            file = file,
            public_id = uuid4().hex,
            folder = folder,
            resource_type = resource_type,
            quality="auto",
            fetch_format="auto")
            
            if result:
                return True, {
                    'success' : True,
                    'public_id' : result['public_id'].split('/')[1],
                    'resource_type' : resource_type,
                    'bytes' : result['bytes'],
                    'secure_url' : result['secure_url'],
                    'display_name' : result['display_name']}
            return False, result
        except Exception as e:
            print(f'Exception: {e}')
            return False, 'Failed to upload file'
