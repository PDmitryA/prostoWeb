from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def helloWorld(request):
    content = 'Hello, world! \n'
    if(request.method == "GET"):
        for i in request.GET.keys():
            content += str(i) + ' = '
            content += request.GET.get(i) + ' \n'

    if(request.method == "POST"):
        for i in request.POST.keys():
            content += str(i) + ' = '
            content += request.POST.get(i) + ' \n'

    return HttpResponse(content, content_type='text/html', status=200)