from django.urls import path
from . import views

app_name = 'cart'  # Uygulama adını tanımla

urlpatterns = [
    # /cart/ -> Sepet detayını göster
    path('', views.cart_detail, name='cart_detail'),  # Sepet detay sayfası

    # /cart/add/1/ -> ID'si 1 olan ürünü sepete ekle
    path('add/<int:product_id>', views.cart_add, name='cart_add'),  # Ürün ekleme sayfası

    # /cart/remove/1/ -> ID'si 1 olan ürünü sepetten çıkar
    path('remove/<int:product_id>', views.cart_remove, name='cart_remove'),  # Ürün çıkarma sayfası
]

