from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path(
        '',
        views.IndexView.as_view(),
        name='index',
    ),
    path(
        'category/',
        views.CategoryView.as_view(),
        name='category',
    ),
    path(
        'product/<slug:slug>/',
        views.ProductView.as_view(),
        name='product',
    ),
    path(
        'cart/',
        views.CartView.as_view(),
        name='cart',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
