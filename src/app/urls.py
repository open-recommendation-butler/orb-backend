from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

urlpatterns = [
    path("", index, name='index'),
    path("admin/", admin.site.urls),
    path("article/", include('article.urls')),
    path("category/", include('category.urls')),
    path("portal/", include('portal.urls')),
    path("topic/", include('topic.urls')),
    path("suggestion/", include('suggestion.urls')),
    path('search/', include('search.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token)
    ]