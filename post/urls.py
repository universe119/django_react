"""
URL configuration for post project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

# 앱이 추가될 때 기본 path 경로와 각 앱 폴더 안쪽의 urls.py를 아래와 같이 등록
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('post_app.urls')),
]

"""
CORS
(Cross-Origin Resources Sharing)은
웹어플리케이션에서 특정 도메인에서 다른 도메인으로 데이터 요청할때 발생하는 보안 문제 해결을 위해 사용

"""