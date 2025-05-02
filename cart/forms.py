from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]  # 1'den 20'ye kadar seçenek

class CartAddProductForm(forms.Form):
    # coerce=int ile gelen değeri integer'a çevirir
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int, label="Adet")

    # override=True ise sepetteki mevcut adedi bu değerle değiştirir, False ise ekler
    # HiddenInput ile kullanıcı görmez ama formla gönderilir.
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)