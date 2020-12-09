from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from main import views
from .views import item_list

app_name ='main'

admin.site.site_title = "MAGLIAMATTA Admin Portal"
admin.site.site_header = "MAGLIAMATTA Administration"
admin.site.index_title = "Welcome to MAGLIAMATTA Portal"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', include('allauth.urls')),

    path('', views.home, name="home"),
    path('base/', views.base, name="base"),
    path('list/', item_list, name="item-list"),

    path('<int:product_id>', views.details, name="details"),

    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
