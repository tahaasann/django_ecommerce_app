from django.urls import path
from . import views

app_name = "products" # URL isim alanı (namespace) tanımlıyoruz

urlpatterns = [
    # / (Ana sayfa) -> Tüm ürünleri listele
    path("", views.product_list, name="product_list"),

    # /category/category-slug/ -> Kategoriye göre ürünleri listele
    path('category/<slug:category_slug>', views.product_list, name='product_list_by_category'),

    # /product/1/product-slug/ -> Üürün detayını göster
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>', views.delete_product, name='delete_product'),

]

