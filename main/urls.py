from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

from django.contrib.sitemaps.views import sitemap
from main.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}


app_name ='main'

admin.site.site_title = "MAGLIAMATTA Admin Portal"
admin.site.site_header = "MAGLIAMATTA Administration"
admin.site.index_title = "Welcome to MAGLIAMATTA Portal"


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name="home"),
    path('base/', views.base, name="base"),
    path('cookie_policy/', views.cookiePolicy, name="cookie_policy"),
    path('privacy_policy/', views.privacyPolicy, name="privacy_policy"),
    path('contact/', views.contactmail, name="contact"),
    path('success/', views.success, name="success"),
    path('info/', views.info, name="info"),



    path('<int:product_id>', views.details, name="details"),
    path('about/', views.about, name="about"),

    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),



    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
