from rest_framework import serializers
from ShadowAiRest.models import Order,Image,ProcessedImage
from django.core.files.base import ContentFile
import uuid
import base64

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=('id', 
                'shadow',
                'ext', 
                'sizeoption',
                'req_height',
                'req_width',
                'responsed')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Image
        fields=('id',
                'name',
                'image', 
                'order')

    def create(self, data, orderid):
        '''
            data[0]:single base64 binary string
            data[1]:dataurl header(include original file format)
        '''
        image_name=str(uuid.uuid4())
        ext=''
        
        if data[1].find('png'):
            ext='.png'
        elif data[1].find('jp'):
            ext='.jpg'
        else:
            ext='bmp'

        result, created = Image.objects.get_or_create(
            name=image_name,
            image=ContentFile(base64.b64decode(data[0]),
            name=image_name+ext),
            order=orderid
            )
        return result

class ProcessedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProcessedImage
        fields=(
            'id',
            'name',
            'image',
            'origin'
        )
    
    def create(self,imagedata,ext,origin_id):
        image_name=str(uuid.uuid4())
        result, created= ProcessedImage.obejcts.get_or_create(
            name=image_name,
            image=ContentFile(imagedata, name=image_name+ext),
            origin=origin_id
            )
        return result