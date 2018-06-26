from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from utils import pagination



# Create your views here.


def login(request):
    if request.method == "GET":
        return render(request, 'login1.html')

    if request.method == "POST":
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        g = request.POST.get("gender")
        f = request.POST.getlist("favor")
        c = request.POST.get("city")

        # 返回obj或None
        user_info_obj = models.UserInfo.objects.filter(username=u, password=p).first()
        if user_info_obj:
            print(user_info_obj)
            return redirect('/myapp/index')
        return render(request, 'login1.html')

from myapp import models
def orm(reauest):
    # 增1
    # models.UserInfo.objects.create(
    #     username='root',
    #     password='123',
    # )

    # 增2
    # user_dict = {
    #     "username": 'Mi',
    #     "password": '123',
    # }
    # models.UserInfo.objects.create(**user_dict)

    # 增3
    # obj = models.UserInfo(username='Alex',password='123')
    # obj.save()

    # 删
    models.UserInfo.objects.filter(id=3).delete()

    # 改
    models.UserInfo.objects.all().update(password='456')

    # 查
    # result = models.UserInfo.objects.all()
    # print(result)



    return HttpResponse('ORM')


def index(request):
    return render(request, 'index2.html')


def user_detail(request, u_id):
    result = models.UserInfo.objects.filter(id=u_id).first()
    return render(request, 'user_info_detail.html', {'user_info': result})


def user_del(request, u_id):
    models.UserInfo.objects.filter(id=u_id).delete()
    return redirect('/myapp/user_info')


def user_edit(request, u_id):
    if request.method == "GET":
        user_obj = models.UserInfo.objects.filter(id=u_id).first()
        return render(request, 'user_edit.html', {'user_obj': user_obj})
    elif request.method == "POST":
        u_id = request.POST.get('u_id')
        u = request.POST.get('username')
        p = request.POST.get('pwd')
        models.UserInfo.objects.filter(id=u_id).update(username=u, password=p)
        return redirect('/myapp/user_info/')


def user_info(request):
    if request.method == "GET":
        user_list = models.UserInfo.objects.all()
        group_list = models.UserGroup.objects.all()
        return render(request, 'user_info.html', {'user_info': user_list, 'group_list': group_list})
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('pwd')
        g_id = request.POST.get('group_id')
        models.UserInfo.objects.create(username=u, password=p, user_group_id=g_id)
        return redirect('/myapp/user_info')



def detail3(request, *args, **kwargs):

    print(kwargs)
    return HttpResponse('{} {} {}'.format(kwargs['h1'], kwargs['h2'], kwargs['h3']))


class Login(View):

    def dispatch(self, request, *args, **kwargs):
        # before
        result = super(Login, self).dispatch(request, *args, **kwargs)
        # after
        return result

    def get(self, request):
        return HttpResponse('Login')

    def post(self, request):
        pass


def paging(request):
    current_pag = int(request.GET.get('p', 1))
    val = request.COOKIES.get('num_per_pag', 10)
    val = int(val)
    data_list = []
    for i in range(1, 200):
        data_list.append(i)
    p_obj = pagination.Page(data_list, current_pag, val)
    data = p_obj.data
    pagination_str = p_obj.pagination_str("/myapp/paging")
    # from django.utils.safestring import mark_safe
    # pagination_str = mark_safe(pagination_str)
    return render(request, 'paging.html', {'data_list': data, 'pagination_str': pagination_str})



########################### cookie ###########################
user_dic = {
    'dachengzi': {'pwd': "123123"},
    'alex': {'pwd': "123"},
}


def clogin(request):
    if request.method == "GET":
        return render(request, 'clogin.html')
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('pwd')
        dic = user_dic.get(u)
        if not dic:
            return render(request, 'clogin.html')
        if dic['pwd'] == p:
            res = redirect('/myapp/cindex/')
            print(res)
            # res.set_cookie('username111',u,max_age=10)
            # import datetime
            # current_date = datetime.datetime.utcnow()
            # current_date = current_date + datetime.timedelta(seconds=5)
            # res.set_cookie('username111',u,expires=current_date)
            res.set_cookie('username111', u)
            res.set_cookie('user_type', "asdfjalskdjf", httponly=True)
            return res
        else:
            return render(request, 'clogin.html')


def cauth(func):
    def inner(request, *args, **kwargs):
        v = request.COOKIES.get('username111')
        if not v:
            return redirect('/myapp/clogin')
        else:
            return func(request, *args, **kwargs)
    return inner

@cauth
def cindex(request):
    v = request.COOKIES.get('username111')
    return render(request, 'cindex.html', {'current_user': v})

from django.views.decorators.csrf import csrf_exempt,csrf_protect


# @csrf_exempt
def slogin(request):
    if request.method == "GET":
        return render(request, 'slogin.html')
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('pwd')
        print(u, p)
        if u == 'root' and p == '123':
            request.session['username'] = u
            request.session['is_login'] = True
            if request.POST.get('expire_time') == '10':
                request.session.set_expiry(10)
            return redirect('/myapp/sindex/')
        else:
            return render(request, 'slogin.html')

def sindex(request):
    if request.session.get('is_login'):
        return render(request, 'sindex.html')
    else:
        return HttpResponse('滚')


def slogout(request):
    request.session.clear()
    return redirect('/myapp/slogin/')


def tmid(request):
    int('xxxx')
    print('in function!')
    return HttpResponse('OK')


from django.views.decorators.cache import cache_page

# 缓存10s
# @cache_page(10)
def cache(request):
    import time
    ctime = time.time()

    return render(request, 'cache.html', {'ctime': ctime})

from myapp.models import UserInfo
def signal(request):
    user_obj = UserInfo(username='root')
    user_obj.save()
    print('save end.')

    user_obj = UserInfo(username='root')
    user_obj = UserInfo(username='root')

    return HttpResponse('test')


from django import forms


# class FM(forms.Form):
#     # user = forms.CharField()
#     # pwd = forms.CharField()
#     # email = forms.EmailField()
#
#     # 字段本身只做认证
#     user = forms.CharField(error_messages={'required': "用户名不能为空"})
#     pwd = forms.CharField(
#         max_length=12,
#         min_length=6,
#         error_messages={'required': "密码不能为空", 'min_length': "密码长度不能小于6", 'max_length': "密码长度不能大于12"})
#     email = forms.EmailField(error_messages={'required': "邮箱不能为空", 'invalid': "邮箱格式不对"})

from django.forms import fields
from django.forms import widgets


class FM(forms.Form):
    # user = forms.CharField()
    # pwd = forms.CharField()
    # email = forms.EmailField()

    # 字段本身只做认证
    user = fields.CharField(
        error_messages={'required': "用户名不能为空"},
        widget=widgets.Input(attrs={'id': 'username'}),
        label="用户名"
        )
    pwd = fields.CharField(
        max_length=12,
        min_length=6,
        error_messages={'required': "密码不能为空", 'min_length': "密码长度不能小于6", 'max_length': "密码长度不能大于12"},
        widget=widgets.PasswordInput(attrs={'id': 'pwd'}),
        # widget=widgets.PasswordInput,

    )
    gender = fields.ChoiceField(
        choices=((1, '男'), (2, '女')),
        initial=2,
        label="性别："
        # widget=widgets.RadioSelect
        # widget=widgets.Select
    )
    # gender = fields.MultipleChoiceField(
    #     choices=((1, '男'), (2, '女')),
    #     initial=2,
    #     label="性别："
    #     # widget=widgets.RadioSelect
    # )
    email = fields.EmailField(error_messages={'required': "邮箱不能为空", 'invalid': "邮箱格式不对"},
                              widget=widgets.Input(attrs={'id': 'em'}))

    f = fields.FileField()
    f_show = fields.FilePathField(path='cache')


def form(request):
    if request.method == "GET":
        dic = {
            "user": "ni",
            "pwd": "1212122",
            "gender": 1,
            "email": 'xx@qq.com',
        }
        obj = FM()
        # obj = FM(initial=dic)
        return render(request, 'form.html', {'obj': obj})

    elif request.method == "POST":
        # print(request.POST)
        obj = FM(request.POST)
        r1 = obj.is_valid()
        if r1:
            print(obj.cleaned_data)
        else:
            print(obj.errors)
            print(obj.errors.as_json())
            # print(obj.errors['user'][0])
            return render(request, 'form.html', {'obj': obj})
        return render(request, 'form.html')


from myapp.models import Users,UserType
def model(request):

    # 正向跨表1
    obj = models.Users.objects.all()
    for i in obj:
        print(i.user, i.pwd, i.ut.name)
    print(''.center(500, '-'))

    # 正向跨表2
    obj1 = Users.objects.values('user', 'pwd', 'ut__name')
    print(obj1, 'obj1')
    for i in obj1:
        print(i['user'], i['pwd'], i['ut__name'])
    print(''.center(500, '*'))

    # 反向跨表查找1
    print('反查1开始'.center(100, '-'))
    obj4 = UserType.objects.all()
    for i in obj4:
        for j in i.users_set.all():
            print(j.user, j.pwd, i.name)
    print('反查1结束'.center(100, '-'))
    # 注意：当 ut = models.ForeignKey(to='UserType', to_field='id', related_name='b') 时，"users_set"被替换成b
    # obj4 = UserType.objects.all()
    # for i in obj4:
    #     for j in i.b.all():
    #         print(j.user, j.pwd, i.name)
    # print(''.center(500, '-'))

    # 反向跨表查找2
    print('反查2开始'.center(100, '-'))
    obj3 = UserType.objects.values('users__user', 'users__pwd', 'name')
    for i in obj3:
        print(i['users__user'], i['users__pwd'], i['name'])
    print('反查1结束'.center(100, '-'))
    # 注意：当 ut = models.ForeignKey(to='UserType', to_field='id', related_name='b') 时，"users"被替换成b
    # obj3 = UserType.objects.values('b__user', 'b__pwd', 'name')
    # for i in obj3:
    #     print(i['b__user'], i['b__pwd'], i['name'])
    # print(''.center(500, '-'))
    # 注意：当 ut = models.ForeignKey(to='UserType', to_field='id', related_query_name='a') 时，"users"被替换成a
    # obj3 = UserType.objects.values('a__user', 'a__pwd', 'name')
    # for i in obj3:
    #     print(i['a__user'], i['a__pwd'], i['name'])
    # print(''.center(500, '-'))


    # print(models.Users.objects.defer('id'))
    # print(models.Users.objects.all())
    for x in models.Users.objects.defer('id'):
        print(x.id, x.pwd)


    return HttpResponse('OK')


from myapp.form import Form1
def form1(request):
    obj = Form1()
    return render(request, 'form1.html', {'obj': obj})