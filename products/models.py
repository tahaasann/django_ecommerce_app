from django.db import models
from django.urls import reverse # URL'leri dinamik oluşturmak için
# Create your models here.
from django.conf import settings
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True) # URL dostu isim

    class Meta:
        ordering = ('name',)
        verbose_name = 'category',
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Kategoriye ait ürünleri listeleyen URL'i döndürür
        return reverse('products:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products_owned', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True) # Stokta var mı?
    created = models.DateTimeField(auto_now_add=True) # Oluşturma tarihi
    updated = models.DateTimeField(auto_now=True) # Güncellenme tarihi

    class Meta:
        ordering = ('name',)
        # Aynı slug'a sahip ürünler farklı kategorilerde olabilir diye düşünerek
        # index_together = (('id','slug'),) # Django yerine constraints kullanmak daha modern olabilir
        indexes = [
            models.Index(fields=['id','slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
            models.Index(fields=['owner']),
        ]

    def save(self, *args, **kwargs):
        # Eğer slug boşsa veya yeni oluşturuluyorsa, name'den otomatik oluştur
        if not self.slug:
            self.slug = slugify(self.name)
            # Benzersizliği sağlamak için ek kontrol gerekebilir (örn: slug + id)
            # Şimdilik basit tutalım. Farklı isimli ürünler aynı slug'a sahip olabilir.
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:product_detail", args=[self.id, self.slug])
    