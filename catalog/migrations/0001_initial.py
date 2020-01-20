# Generated by Django 2.2.6 on 2019-10-22 19:02

import catalog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('type', models.CharField(choices=[('sales channel', 'sales channel'), ('country', 'country')], max_length=255)),
                ('object_id', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('-created_at', '-updated_at'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'ordering': ('-created_at', '-updated_at'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SalesChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('-created_at', '-updated_at'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('default_availability', models.CharField(choices=[('available', 'available'), ('unavailable', 'unavailable')], max_length=255)),
            ],
            options={
                'ordering': ('-created_at', '-updated_at'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SupplierArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('article', models.CharField(max_length=255, verbose_name=catalog.models.Article)),
                ('supplier_reference_number', models.CharField(max_length=255)),
                ('stock', models.IntegerField(default=0)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Supplier')),
            ],
            options={
                'ordering': ('-created_at', '-updated_at'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SupplierSalesChannelArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('price_old', models.DecimalField(decimal_places=2, max_digits=9)),
                ('sales_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.SalesChannel')),
                ('supplier_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.SupplierArticle')),
            ],
            options={
                'ordering': ('-created_at', '-updated_at'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SupplierMarketAvailability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('supplier', models.CharField(max_length=255)),
                ('availability', models.CharField(choices=[('available', 'available'), ('unavailable', 'unavailable')], max_length=255)),
                ('markets', models.ManyToManyField(to='catalog.Market')),
            ],
            options={
                'ordering': ('-created_at', '-updated_at'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Product')),
            ],
            options={
                'ordering': ('-created_at', '-updated_at'),
                'abstract': False,
            },
        ),
    ]
