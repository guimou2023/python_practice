from django.shortcuts import render, HttpResponse,redirect
from django.views import View


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
        print(user_list)
        return render(request, 'user_info.html', {'user_info': user_list})
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('pwd')
        models.UserInfo.objects.create(username=u, password=p)
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