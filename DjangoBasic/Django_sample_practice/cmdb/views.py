from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect


def login(request):

    error_msg = ""
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        print(user, pwd)
        if user == 'root' and pwd == '123':
            return redirect('/home')
        else:
            error_msg = "用户名活密码错误"

    return render(request, 'login.html', {'error_msg': error_msg})

USER_LIST = [
    {'id': 1, 'username': 'alex', 'email': 'asdfasdf', "gender": '男'},
    {'id': 2, 'username': 'eriuc', 'email': 'asdfasdf', "gender": '男'},
    {"id": 3,'username': 'seven', 'email': 'asdfasdf', "gender": '男'},
]


def home(request):
    if request.method == "POST":
        u = request.POST.get('username')
        e = request.POST.get('email')
        g = request.POST.get('gender')
        num = len(USER_LIST) + 1
        temp_data = {"id": str(num), 'username': u, 'email': e, "gender": g}
        USER_LIST.append(temp_data)
    return render(request, 'home.html', {'user_list': USER_LIST})
