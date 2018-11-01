from django.contrib import admin
from .models import *
# Register your models here.



class GoodsAdmin(admin.ModelAdmin):
    #指定展示的字段
    list_display = ('title','goodsType','price','spec')
    #指定右侧显示的过滤器
    list_filter = ('goodsType',)
    search_fields = ('title',)

class CityAdmin(admin.ModelAdmin):
    list_display = ('cities',)
    search_fields = ('cities',)

    #指定在上方显示的搜索字段



admin.site.register(GoodsType)
admin.site.register(Goods,GoodsAdmin)
admin.site.register(City,CityAdmin)