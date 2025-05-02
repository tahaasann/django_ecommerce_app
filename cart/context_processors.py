from .cart import Cart

def cart(request):
    # Sepeti her şablonda erişilebilir kılmak için context processor
    return {'cart': Cart(request)}