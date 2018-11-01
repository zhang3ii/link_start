from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^login/$',login_in,name='lo'),
    url(r'^register/$',register,name='re'),
    url(r'^check_uphone/$',check_uphone_data),
    url(r'^$',index_views),
    url(r'^check_login/$',check_login_views),
    url(r'^logout/$',logout),
    url(r'^load_type_goods/$',type_goods_views),
    url(r'^add_cart/$',add_cart_views),
    url(r'^cart_views/$',cart_views),
]