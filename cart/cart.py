# View'ları temiz tutmak için sepet işlemlerini (ekleme, çıkarma, hesaplama) bir sınıf içinde toplayalım.
# Neden sınıf? Sepetle ilgili tüm mantığı (session'dan alma, ekleme, silme, hesaplama) tek bir yerde toplar, kod tekrarını önler ve view'lar daha okunabilr hale getirir.
from decimal import Decimal
from django.conf import settings
from products.models import Product # Product modelini kullanacağız

class Cart:
    def __init__(self, request):
        # Sepeti başlat
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart:
            # oturumda boş bir sepeti kaydet
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        # Ürünü sepete ekle veya güncelle
        product_id = str(product.id) # Session key'leri string olmalı
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Kaydedildiğinden emin olmak için session'ı "modified(değiştirildi)" olarak işaretle
        self.session.modified = True
    
    def remove(self, product):
        # Ürünü sepetten çıkar
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        # Sepetteki ürünler üzerinde gezinin ve ürünleri db'den alın.
        product_ids = self.cart.keys()
        # ürün nesnelerini al ve sepete ekle
        products = Product.objects.filter(id__in=product_ids) # __in ile birden fazla id alabiliriz
        cart = self.cart.copy() # Sepeti kopyala, böylece orijinal sepeti değiştirmeyiz
        for product in products:
            cart[str(product.id)]['product'] = product # Ürün nesnesini sepete ekle

        for item in cart.values():
            item['price'] = Decimal(item['price']) # Fiyatı Decimal tipine çevir
            item['total_price'] = item['price'] * item['quantity']
            yield item # yield ile generator yapıyoruz, hafıza dostu

    def __len__(self):
        # Sepetteki ürün sayısını döndür
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        # Sepetteki toplam fiyatı döndür
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        # Sepeti temizle
        del self.session[settings.CART_SESSION_ID]
        self.save()