from django.db import models


class Products(models.Model):
    product_url_image = models.TextField(verbose_name="Product Image URL")
    product_url = models.TextField(verbose_name="Product URL")
    product_url_created_at = models.DateField(verbose_name="Created Date")
    consult_date = models.DateField(verbose_name="Consultation Date")
    sales_of_the_day = models.IntegerField(verbose_name="Sales of The Day")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
