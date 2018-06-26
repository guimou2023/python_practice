from django.shortcuts import render, redirect, HttpResponse

from myapp1 import models
# Create your views here.


def orm(request):
    v1 = models.Business.objects.all()
    # <QuerySet [<Business: Business object>, <Business: Business object>, <Business: Business object>]>

    v2 = models.Business.objects.all().values('id', 'caption', 'EnName')
    # <QuerySet [{'id': 1, 'caption': '技术部', 'EnName': None}, {'id': 2, 'caption': '运营部', 'EnName': None}, {'id': 3, 'caption': '销售部', 'EnName': None}]>

    v3 = models.Business.objects.all().values_list('id', 'caption', 'EnName')
    # <QuerySet [(1, '技术部', None), (2, '运营部', None), (3, '销售部', None)]>


    return render(request, 'business.html', {'v1': v1, 'v2': v2, 'v3': v3 })


def host(request):

    if request.method == "GET":
        v1 = models.Host.objects.all()
        ca_list = models.Business.objects.all()
        return render(request, 'host.html', {'v1': v1, 'ca_list': ca_list })
    if request.method == "POST":
        host_name = request.POST.get('host_name')
        ip = request.POST.get('ip')
        port = request.POST.get('port')
        b_id = request.POST.get('b_id')
        models.Host.objects.create(hostname=host_name, ip=ip, port=port, b_id=b_id)
        return redirect('/myapp1/host')


def ajax_submit(request):
    import json
    res = {'status': "True", 'error': "None", 'data': "None"}
    try:
        if request.method == "POST":
            hostname = request.POST.get('host_name')
            ip = request.POST.get('ip')
            port = request.POST.get('port')
            b_id = request.POST.get('b_id')
            print('hostname', hostname)
            print('ip', ip)
            print('port', port)
            print('b_id', b_id)

            if hostname and len(hostname) > 5:
                models.Host.objects.create(hostname=hostname, ip=ip, port=port, b_id=b_id)
            else:
                res['status'] = False
                res['error'] = "主机名不合法。"

    except Exception as e:
        res['status'] = False
        res['error'] = "请求异常"
    return HttpResponse(json.dumps(res))


def ajax_delete(request):
    if request.method == "POST":
        nid = request.POST.get('nid')
        models.Host.objects.filter(nid=nid).delete()
        return HttpResponse("删除成功")


def edit_submit(request):
    if request.method == "POST":
        nid = request.POST.get('nid')
        b_id = request.POST.get('b_id')
        models.Host.objects.filter(nid=nid).update(b_id=b_id)
        return HttpResponse("test")


def app(request):
    import json
    if request.method == "GET":
        print(request.path_info)
        print(request.resolver_match)
        app_list = models.Application.objects.all()
        h_list = models.Host.objects.all()
        return render(request, 'app.html', {'app_list': app_list, 'host_list': h_list})
    elif request.method == "POST":
        res = {'status': "True", 'error': "None", 'data': "None"}
        try:
            app_name = request.POST.get('app_name')
            host_list = request.POST.getlist('host_list')
            app_obj = models.Application.objects.create(name=app_name)
            app_obj.r.add(*host_list)
        except Exception as e:
            res['status'] = False
            res['error'] = "请求异常"
        return HttpResponse(json.dumps(res))


def app_add_host(request):
    pass
