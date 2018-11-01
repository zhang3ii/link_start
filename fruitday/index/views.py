import json

from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from .forms import *
# Create your views here.



def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:

        uphone = request.POST['uphone']

        upwd = request.POST['upwd']
        uname = request.POST['uname']
        uemail = request.POST['uemail']
        dic = {
            'uphone':uphone,
            'upwd':upwd,
            'uname':uname,
            'uemail':uemail,
        }
        obj = User(**dic)
        obj.save()
        request.session['uid'] = obj.id
        request.session['uphone'] = obj.uphone
        return redirect('/')

def login_in(request):
    # form = LoginForm()
    # return render(request,'login.html',locals())

    #判断 get 请求还是 post 请求
    if request.method == 'GET':
        #获取来访地址,如果没有则设置为/
        url = request.META.get('HTTP_REFERER','/')

        if 'uid' in request.session and 'uphone' in request.session:
            #有登录信息保存在session
            #从哪来回哪去
            resp = HttpResponseRedirect(url)
            return resp
        else:
            #没有登录信息保存在session,继续判断cookies中是否有登录信息
            if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
                #cookies中有登录信息  - 曾经记住过密码
                #将cookies中的信息保存出来保存进session,再返回到首页
                uid = request.COOKIES['uid']
                uphone = request.COOKIES['uphone']
                request.session['uid'] = uid
                request.session['uphone'] = uphone
                resp = redirect(url)
                return resp
            else:
                #cookies中没有登录信息  - 去往登录页
                form = LoginForm()
                #将来访地址保存进cookies中
                resp = render(request,'login.html',locals())
                resp.set_cookie('url',url)
                return resp


    else:
        #post请求  - 实现登录操作
        #获取手机号和密码
        uphone = request.POST['uphone']
        upwd = request.POST['upwd']
        #判断手机号和密码是否存在(登录是否成功)

        users = User.objects.filter(uphone=uphone,upwd=upwd)
        if users:
            #登录成功
            request.session['uid'] = users[0].id
            request.session['uphone'] = uphone
            #申明相应对象:响音一句话'登录成功'
            #声明响应对象:从哪来回哪去
            url = request.COOKIES.get('url','/')
            resp = redirect(url)
            if 'url' in request.COOKIES:
                resp.delete_cookie('url')

            #将url从cookie删除出去            resp = HttpResponse('登录成功')
            #判断是否要存进cookies
            if 'isSaved' in request.POST:
                expire = 60*60*24
                resp.set_cookie('uid',users[0].id,expire)
                resp.set_cookie('uphone',uphone,expire)
            return resp

        else:
            form = LoginForm()
            return render(request,'login.html',locals())
            #登录失败


def check_uphone_data(request):
    #接收前段传递过来的数据 - uphone
    uphone = request.GET['uphone']
    user = User.objects.filter(uphone = uphone)
    if user:
        status = 1
        msg = '手机号码已经存在'
    else:
        status = 0
        msg = '可以使用的手机号码'

    dic = {
        'status':status,
        'msg':msg,
    }

    return HttpResponse(json.dumps(dic))

def index_views(request):
    return render(request,'ym.html')


#检查session 中是否有登录信息,如果有获取对应数据的uname值
def check_login_views(request):
    if 'uid' in request.session and 'uphone' in request.session:
        loginStatus = 1
        #通过uid的值来过去对应的uname
        id = request.session['uid']
        uname = User.objects.get(id=id).uname
        dic = {
            'loginStatus':loginStatus,
            'uname':uname
        }

        return HttpResponse(json.dumps(dic))
    else:
        dic = {
            'loginStatus':0
        }
        return HttpResponse(json.dumps(dic))

def logout(request):
    if 'uid' in request.session and 'uphone' in request.session:
        del request.session['uid']
        del request.session['uphone']
        #构建响应对象:那发的退出请求,则返回到哪里
        url = request.META.get('HTTP_REFERER','/')
        resp = HttpResponseRedirect(url)
        if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
            resp.delete_cookie('uid')
            resp.delete_cookie('uphone')
        return resp
    return redirect('/')

#加载所有的商品类型以及对应的每个类型下的前10条数据
def type_goods_views(request):
    all_list = []
    #加载所有的商品类型
    types = GoodsType.objects.all()
    for type in types:
        type_json = json.dumps(type.to_dict())
            #获取 type_json 类型下的最新的10条数据
        g_list = type.goods_set.filter(isActive=True).order_by('-id')[0:10]
        #将g_list转换为json
        g_list_json = serializers.serialize('json',g_list)
        #将type_json和list_json封装到一个字典中
        dic = {
            'type':type_json,
            'goods':g_list_json,
        }
        #将dic字典追加到all_list中
        all_list.append(dic)
    return HttpResponse(json.dumps(all_list))


#将商品添加至购物车 或更新现有商品的数量
def add_cart_views(request):
    #获取商品id,获取用户id,购买数量默认为1
    good_id = request.GET['gid']
    user_id = request.session['uid']
    ccount = 1
    #查看购物车中是否有相同用户购买的相同商品
    cart_list = CatInfo.objects.filter(user_id=user_id,goods_id=good_id)

    if cart_list:
        #已经有相同的用户购买过相同的产品了,更新商品数量
        cartinfo = cart_list[0]
        cartinfo.ccount = cartinfo.ccount + ccount
        cartinfo.save()
        dic = {
            'static':0,
            'statusText':'更新数量成功'
        }
    else:
        #没有对应的用户以及对应的商品
        cartinfo = CatInfo()
        cartinfo.user_id = user_id
        cartinfo.goods_id = good_id
        cartinfo.ccount = ccount
        cartinfo.save()
        dic = {
            'status':1,
            'statusText':'添加购物车成功'
        }
    return HttpResponse(json.dumps(dic))


def cart_views(request):
    try:
        user_id = request.session['uid']
        carts = CatInfo.objects.filter(user_id=user_id,goods__isShow=True)

    except:
        return redirect('/')
    return render(request,'cart.html',locals())



