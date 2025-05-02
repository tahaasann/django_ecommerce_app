from django.shortcuts import render, redirect
from django.urls import reverse_lazy # Redirect için lazy versiyon
from django.contrib.auth.forms import UserCreationForm # Hazır kayıt formu
from django.contrib.auth.decorators import login_required # Giriş yapmış kullanıcıları kontrol etmek için

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # Kullanıcıyı otomatik oluşturur ve kaydeder

            # Başarılı kayıttan sonra giriş sayfasına yönlendiriyoruz
            return redirect("login") # veya reverse_lazy("login") kullanabiliriz
    
    else: # GET request ise boş form göster
        form = UserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form':form})

@login_required # Bu decorator, sadece giriş yapmış kullanıcıların bu view'a erişmesini sağlar
def profile(request):
    # Kullanıcı bilgilerini şablona gönderebiliriz (gerçi user zaten context'te var)
    context = {
        'user': request.user,
    }
    return render(request, 'accounts/profile.html', context)