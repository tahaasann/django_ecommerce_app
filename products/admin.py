from django.contrib import admin
from .models import Category, Product
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} # name yazarken slug'ı otomatik doldur


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category'] # Filtreleme seçenekleri
    list_editable = ['price','available'] # Listede direkt düzenlenebilir alanlar
    prepopulated_fields = {'slug': ('name',)} # name yazarken slug'ı otomatik doldur
    search_fields = ['name','description'] # Arama çubuğu ekler