# Generated by Django 4.0.6 on 2022-07-13 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_url_image', models.URLField(verbose_name='Product Image URL')),
                ('product_url', models.URLField(verbose_name='Product URL')),
                ('product_url_created_at', models.DateField(verbose_name='Created Date')),
                ('consult_date', models.DateField(unique=True, verbose_name='Consultation Date')),
                ('sales_of_the_day', models.IntegerField(verbose_name='Sales of The Day')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]
