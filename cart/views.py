from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST # Sadece POST isteklerini kabul etmek için
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.

@require_POST # Sadece POST isteklerini kabul et
def cart_add(request, product_id):
    cart = Cart(request) # Session'dan sepeti al veya oluştur
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST) # Gönderilen POST verisiyle formu oluştur
    if form.is_valid(): # Form geçerliyse
        cd = form.cleaned_data # Formdan temizlenmiş (valiated) veriyi al (bir dict)
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        
        # Başarılı eklemeden sonra sepet detay sayfasına yönlendir
        return redirect('cart:cart_detail')
    
    else:
        # Form geçerli değilse: Genellikle bu senaryoda ürün detayına geri dönüp hatayı göstermek 
        # iyi olabilir, ama şimdilik sepet detayına yönlendiriyoruz.
        return redirect('cart:cart_detail') 
    

@require_POST # Sadece POST isteklerini kabul et
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request) # Session'dan sepeti al veya oluştur
    # Sepet detayında ürün adetlerini güncelleyebilmek için formu ekleyelim
    # Her sepet öğresi için formu oluşturup şablonda gösterebilriiz.
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True}) # Formu sepete ekle
    return render(request, 'cart/detail.html', {'cart': cart}) # Sepet detay sayfasını render et