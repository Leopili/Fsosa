from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField

# Category Model
class Category(models.Model):
    title = models.CharField(max_length=300)
    slug = AutoSlugField(populate_from=['title'])

   
    class Meta:
        ordering = ["title"]
        verbose_name = ("Categoria")
        verbose_name_plural = ("Categorias")

    def __str__(self):
        return self.title
    


#Product Model
class  Product(models.Model):
    name = models.CharField(max_length=300)
    slug = AutoSlugField(populate_from=['name'])
    categories = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)
    preview_text = models.TextField(max_length=200, verbose_name='Preview Text')
    detail_text = models.TextField(max_length=1000, verbose_name='Detail Text')
    price = models.FloatField()
    

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = ("Producto")
        verbose_name_plural = ("Productos")


    def get_absolute_url(self):
        return reverse("mainapp:product", kwargs={
            'slug': self.slug
        })