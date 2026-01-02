from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View


class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
    def post(self, request):
        logout(request)
        return redirect('home')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/logout/', MyLogoutView.as_view(), name='logout'), 
    path('auth/', include('django.contrib.auth.urls')), 
    path('users/', include('users.urls')),
    path('', include('posts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)