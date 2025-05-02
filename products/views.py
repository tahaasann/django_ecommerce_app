from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Category, Product
from .forms import ProductForm
from cart.forms import CartAddProductForm
from django.utils.text import slugify

# Sepet formu için import ekleyeceğiz:
from cart.forms import CartAddProductForm

# Create your views here.
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True) # Sadece mevcut ürünler
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    
    # Sepet formu her ürün için oluşturulacak (bunu detail view'a taşıyabiliriz)
    # cart_product_form = CartAddProductForm() # Her ürün listesi için değil, detayda lazım.

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        # 'cart_product_form': cart_product_form
    }

    return render(request, 'products/product/list.html', context=context)

def product_detail(request, id, slug):
    # Hem ID hem slug ile ürünü bulmak daha garanti (PK + Okunaklı URL)
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    # Ürün detay sayfasında sepete ekleme formu:
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
    }
    return render(request, 'products/product/detail.html', context=context)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            # Henüz veritabanına kaydetme, owner'ı ekleyeceğiz
            new_product = form.save(commit=False)

            # Owner'ı o an giriş yapmış kullanıcı olarak ata
            new_product.owner = request.user

            # Slug'ı otomatik oluştur (modeldeki save metodunda da var ama burada da olabilir)
            

            new_product.save()
            

            try:
                # Ürünün ID'si ve slug'ı ile URL'i oluşturmayı dene
                redirect_url = reverse('products:product_detail', args=[new_product.id, new_product.slug])
                messages.success(request, 'Ürün başarıyla eklendi!')

                return redirect(redirect_url)
            
            except Exception as e:
                # URL oluşturulamazsa (beklenmedik bir durum), hata mesajı ver ve listeye dön.
                messages.error(request, f"Ürün eklendi ancak detay sayfasına yönlendirilemedi: {e}")

                return redirect('products:product_list')

            
        
        else:
            messages.error(request, 'Formda hatalar var. Lütfen kontrol edin.')
    
    else: # GET request ise boş fom göster
        form = ProductForm()
    
    return render(request, 'products/add_edit_product.html', {'form': form, 'page_title': 'Yeni Ürün Ekle'})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Sadece ürün sahibi düzenleyebilir
    if product.owner != request.user:
        raise PermissionDenied("Bu ürünü düzenleme yetkiniz yok.")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product) # instance ile formu doldur
        if form.is_valid():
            form.save() # Varolan instance güncellenir
            messages.success(request, 'Ürün başarıyla güncellendi!')
            return redirect(product.get_absolute_url())
        else:
            messages.error(request, 'Formda hatalar var. Lütfen kontrol edin.')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/add_edit_product.html', {'form': form, 'product': product, 'page_title': 'Ürünü Düzenle'})

@login_required
@require_POST # Sadece POST isteği ile çalışsın (güvenlik)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Sadece ürün sahibi silebilir
    if product.owner != request.user:
        messages.error(request, 'Bu ürünü silme yetkiniz yok.')
        raise PermissionDenied("Bu ürünü silme yetkiniz yok.") # Veya redirect

    product_name = product.name # Silmeden önce ismi alalım
    product.delete()
    messages.success(request, f'"{product_name}" ürünü başarıyla silindi.')
    # Ana sayfaya veya kullanıcının ürünlerim sayfasına yönlendirilebilir
    return redirect('products:product_list')