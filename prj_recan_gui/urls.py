"""prj_recan_gui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path, include
from dotenv import load_dotenv


load_dotenv()


ADMIN_URL = os.environ['ADMIN_URL']

urlpatterns = [
    path(ADMIN_URL, admin.site.urls),
    path("", include("app_recan_gui.urls")),
]


handler500 = 'pages.views.internal_server_error'

