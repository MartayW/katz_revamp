from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path ,include
from .views import logoutuser


# Import all methods from views.py
from . import views

# This is a list of the URL path names (webpages) and their corresponding "view" name.
# The view name is the name of the matching method from the views.py file.
urlpatterns = [
    path ('admin/', admin.site.urls),
    path('index', views.index, name='index'),
    path('kittens/', views.kittens, name='kittens'),
    path('kittens/purchase_direct/<int:id>/<int:id2>', views.kittens_purchase, name='purchase_direct'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('', views.login_page, name='login_page'),
    path('cat_register/', views.cat_register, name='cat_register'),
    path('query_test/', views.query_test, name='query_test'),
    path('logout/', logoutuser, name='logout'),



]