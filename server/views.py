from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
import requests
# Create your views here.

data_dict = {}
CLIENT_ID = '123456789'


def get_code():
    return '1234'


def get_access_token():
    return {
            'access_token': '6789',
            'expire_in': 3600
        }


def authorize(request):
    client_id =  request.GET.get('client_id')
    response_type = request.GET.get('response_type')
    uri = request.GET.get('redirect_uri')
    if client_id and response_type and uri:
        if request.method == 'GET':
            client_info = data_dict[client_id] = {}
            client_info['uri'] = uri
            return render(request, 'authorize.html')
        elif request.method == 'POST':
            aggree = request.POST.get('aggree')
            if aggree:
                code = get_code()
                data_dict[client_id]['code'] = code
                return HttpResponseRedirect(uri+'?code=%s' % code)
            return HttpResponse('gun')
        return HttpResponse('请求方法错误')
    return HttpResponse('url错误')


def access_token(request):
    client_id = request.GET.get('client_id')
    code = request.GET.get('code')
    if data_dict[client_id]['code'] == code:
        token = get_access_token()
        return JsonResponse(token)
    return HttpResponse('不合法code')


def client(request):
    if request.GET.get('code'):
        code = request.GET.get('code')
        url = 'http://localhost:8002/oauth/access_token?client_id=%s&code=%s' % (CLIENT_ID, code)
        result = requests.get(url)
        print(result.content)
        return HttpResponse(result)
    return HttpResponseRedirect('/oauth/authorize/?client_id=%s&response_type=%s&redirect_uri=%s' % (CLIENT_ID, 'code', 'http://localhost:8002/oauth/client/'))