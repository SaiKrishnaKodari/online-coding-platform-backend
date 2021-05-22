from django.contrib import admin
from django.urls import path
from compiler import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('questions',views.questions),
    path('problem/<str:title>/<str:id>',views.code),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)