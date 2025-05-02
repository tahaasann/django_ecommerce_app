from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

        # Formda gösterilecek alanlar
        fields = ['category', 'name', 'image', 'description', 'price', 'available']

        
        widgets = {
            'description' : forms.Textarea(attrs={'rows': 4}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Fiyat sıfırdan büyük olmalıdır.")
        return price