from django.shortcuts import render, HttpResponse
from django.views import View

# Create your views here.

HOST_DICT = {
    '1': {'ip': '172.21.0.1', 'area': 'bj', 'user': 'root'},
    '2': {'ip': '172.21.0.1', 'area': 'bj', 'user': 'root'},
    '3': {'ip': '172.21.0.1', 'area': 'bj', 'user': 'root'},
    '4': {'ip': '172.21.0.1', 'area': 'bj', 'user': 'root'},
    '5': {'ip': '172.21.0.1', 'area': 'bj', 'user': 'root'},
}

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')

    if request.method == "POST":
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        g = request.POST.get("gender")
        f = request.POST.getlist("favor")
        c = request.POST.get("city")
        # print(u, p, g, f, c)

        # wc = request.POST.getlist("work_city")
        # print(wc)

        # fname = request.POST.get("fname")
        # print('name:', fname, type(fname))

        file_obj = request.FILES.get("fname")
        print('name1:', file_obj, 'obj_name:{}'.format(file_obj.name), type(file_obj))
        for i in file_obj.chunks():
            f = open('upload/{}'.format(file_obj.name),'wb')
            f.write(i)
            f.close()
        return render(request, 'login.html')


def index(request):
    return render(request, 'index.html', {'host_dict': HOST_DICT})


def index1(request):
    return render(request, 'index1.html', {'host_dict': HOST_DICT})


def detail(request):
    host_id = request.GET.get("host_id")
    host_detail_info = HOST_DICT.get(host_id)
    return render(request, 'detail.html', {'host_detail_info': host_detail_info})


def detail1(request, h_id1):
    # host_id = request.GET.get("host_id")
    # host_detail_info = HOST_DICT.get(host_id)
    # return render(request, 'detail.html', {'host_detail_info': host_detail_info})
    return HttpResponse('{}'.format(h_id1))


def detail2(request, h_id1, h_id2):
    # host_id = request.GET.get("host_id")
    # host_detail_info = HOST_DICT.get(host_id)
    # return render(request, 'detail.html', {'host_detail_info': host_detail_info})
    return HttpResponse('{} {}'.format(h_id1, h_id2))


# def detail3(request, h2, h1, h3):
#     # host_id = request.GET.get("host_id")
#     # host_detail_info = HOST_DICT.get(host_id)
#     # return render(request, 'detail.html', {'host_detail_info': host_detail_info})
#     return HttpResponse('{} {} {}'.format(h1, h2, h3))


def detail3(request, *args, **kwargs):
    # host_id = request.GET.get("host_id")
    # host_detail_info = HOST_DICT.get(host_id)
    # return render(request, 'detail.html', {'host_detail_info': host_detail_info})
    # print(args)
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