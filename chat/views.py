from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings

from .models import Chat



def ChatPage(request):
    c = Chat.objects.all()
    return render(request, "chat.html", {'chatpage': 'active', 'chat': c})

def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        c = Chat(user=request.user, message=msg)
        if msg != '':
            c.save()
        return JsonResponse({ 'msg': msg, 'user': c.user.username })
    else:
        return HttpResponse('Request must be POST.')

def Messages(request):
    c = Chat.objects.all()
    return render(request, 'messages.html', {'chat': c})