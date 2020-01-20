from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse_lazy
from django.utils.timezone import now

import pycountry

from shared.models import TimestampedModel


def upload_to(instance, filename):
    model = type(instance)
    return '{app_label}/{model_name}/{year}/{month}/{day}/{hour}/{minute}/{second}/{filename}'.format(
        app_label=model._meta.app_label,
        model_name=model._meta.model_name,
        year=instance.updated_at.year,
        month=instance.updated_at.month,
        day=instance.updated_at.day,
        hour=instance.updated_at.hour,
        minute=instance.updated_at.minute,
        second=instance.updated_at.second,
        filename=filename,
    )


class Product(TimestampedModel, models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    attributes = GenericRelation('attributes.ObjectAttributeValue', content_type_field='object_type')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('shop:product', args=(self.slug,))


class ProductImage(TimestampedModel, models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to)

    def __str__(self):
        return str(self.image)


class Article(TimestampedModel, models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attributes = GenericRelation('attributes.ObjectAttributeValue', content_type_field='object_type')

    def __str__(self):
        return ' '.join(rel.attribute_value.name for rel in self.attributes.iterator())


class SalesChannel(TimestampedModel, models.Model):
    ONLINE_SHOP = 'online shop'
    PHYSICAL_SHOP = 'physical shop'

    TYPES = (
        (ONLINE_SHOP, ONLINE_SHOP),
        (PHYSICAL_SHOP, PHYSICAL_SHOP)
    )

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, default=ONLINE_SHOP)

    def __str__(self):
        return self.name


class Market(TimestampedModel, models.Model):
    SALES_CHANNEL = 'sales channel'
    COUNTRY = 'country'

    TYPES = (
        (SALES_CHANNEL, SALES_CHANNEL),
        (COUNTRY, COUNTRY)
    )

    type = models.CharField(max_length=255, choices=TYPES)
    object_id = models.CharField(max_length=255)

    @property
    def object(self):
        if self.type == self.SALES_CHANNEL:
            return SalesChannel.objects.get(pk=self.object_id)
        elif self.type == self.COUNTRY:
            return pycountry.countries.get(alpha_3=self.object_id)
        else:
            raise NotImplementedError(self.type)

    @classmethod
    def get_object_id_choices(cls, type):
        if type == cls.SALES_CHANNEL:
            return SalesChannel.objects.values_list('pk', 'name')
        elif type == cls.COUNTRY:
            return [
                (country.alpha_3, country.name)
                for country
                in pycountry.countries
            ]
        else:
            raise NotImplementedError(type)

    def __str__(self):
        object = self.object
        return self.object.name


class Supplier(TimestampedModel, models.Model):
    AVAILABLE = 'available'
    UNAVAILABLE = 'unavailable'

    AVAILABILITIES = (
        (AVAILABLE, AVAILABLE),
        (UNAVAILABLE, UNAVAILABLE)
    )

    name = models.CharField(max_length=255)
    default_availability = models.CharField(max_length=255, choices=AVAILABILITIES, default=AVAILABLE)


class SupplierMarketAvailability(TimestampedModel, models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    markets = models.ManyToManyField(Market)
    availability = models.CharField(max_length=255, choices=Supplier.AVAILABILITIES, default=Supplier.AVAILABLE)


class SupplierArticle(TimestampedModel, models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    supplier_reference_number = models.CharField(max_length=255)
    stock = models.IntegerField(default=0)


class SupplierSalesChannelArticle(TimestampedModel, models.Model):
    supplier_article = models.ForeignKey(SupplierArticle, on_delete=models.CASCADE)
    sales_channel = models.ForeignKey(SalesChannel, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    price_old = models.DecimalField(max_digits=9, decimal_places=2)
