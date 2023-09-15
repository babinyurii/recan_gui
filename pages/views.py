from django.shortcuts import render

def internal_server_error(request, *args, **argv):
    return render(request, 'custom_500.html', status=500)