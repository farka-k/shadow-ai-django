from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from ShadowAiRest.models import Order,Image
from ShadowAiRest.serializers import OrderSerializer,ImageSerializer
from rest_framework.decorators import api_view
import json,base64
import os.path
from ShadowAiDjango.settings import MEDIA_ROOT,STATIC_URL,BASE_DIR
import tensorflow as tf

# Create your views here.
@api_view(['POST'])
def image(request):
    #POST images with new order
    if request.method=='POST':
        image_data=JSONParser().parse(request)
        new_order=Order.objects.create()
        image_data_zip=list(zip(image_data['img'],image_data['type']))
        try:
            for item in image_data_zip:
                image_serializer=ImageSerializer().create(item,new_order.id)
                if image_serializer.is_valid():
                    image_serializer.save()
                else:
                    return JsonResponse({"message":"error"}, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse({"id":new_order.id},status=status.HTTP_201_CREATED)
        except:
            i=Image.objects.filter(order=new_order.id)
            i.delete()
            new_order.delete()
            return JsonResponse({"message":"no"},status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def order_detail(request, batch_id):
    #find all images with order==batch_id, apply model to response
    order_data=JSONParser().parse(request)
    order_data['id']=int(batch_id)
    if order_data['sizeoption']==0:
        order_data['req_height']=-1
        order_data['req_width']=-1
    print(order_data)
    order=Order.objects.get(id=batch_id)
    order_serializer=OrderSerializer(order,data=order_data)
    if order_serializer.is_valid():
        order_serializer.save()

    #images=list(Image.objects.filter(order=batch_id))
    #for i in images:

    
    try:
        images=list(Image.objects.filter(order=batch_id))
        base64src=[]
        for i in images:
            with open(os.path.join(MEDIA_ROOT,str(i.image)),"rb") as img:
                data=base64.b64encode(img.read()).decode('utf-8')
                base64src.append(data)
        res={"result":base64src}
        return JsonResponse(res,status=status.HTTP_200_OK)
    except Image.DoesNotExist:
        return JsonResponse({'message':'Unable to find correct Images'}, status=status.HTTP_404_NOT_FOUND)