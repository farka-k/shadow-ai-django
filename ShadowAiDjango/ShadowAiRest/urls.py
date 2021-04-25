from django.conf.urls import url
from ShadowAiRest import views

urlpatterns=[
    url(r'^api/images$',views.image),
    #url(r'^api/images/(?P<pk>[0-9]+)$',),
    #url(r'^api/orders/(?P<pk>[0-9]+)$',),
    #url(r'^api/images/(?P<pk>[0-9]+)/conv$',),
    url(r'^api/orders/(?P<batch_id>[0-9]+)/conv$',views.order_detail)
]