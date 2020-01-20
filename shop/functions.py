from dataclasses import dataclass, field
from decimal import Decimal
from typing import List

from django.utils.functional import cached_property

import pycountry

from catalog.models import (
    Article,
    Market,
    SalesChannel,
    Supplier,
    SupplierArticle,
    SupplierMarketAvailability,
    SupplierSalesChannelArticle,
)
from shop.models import CartItem, Customer


@dataclass(frozen=True)
class Item:
    article: Article
    unit_price: Decimal
    quantity: int
    line_total: Decimal
    sold_out: bool


@dataclass(frozen=True)
class Cart:
    customer: Customer
    sales_channel: SalesChannel
    total: Decimal
    can_continue_to_checkout: bool
    items: List[CartItem] = field(default_factory=list)

    @classmethod
    def get(cls, customer, sales_channel):
        if not isinstance(customer, Customer):
            customer = Customer.objects.get(pk=customer)

        cart_items = list(
            CartItem.objects.select_related(
                'article__product',
            ).prefetch_related(
                'article__product__productimage_set',
            ).filter(
                customer=customer,
                sales_channel=sales_channel,
                quantity__gt=0,
            )
        )

        supplier_market_availabilities = SupplierMarketAvailability.objects.prefetch_related(
            'markets',
        ).filter(
            markets__type=Market.SALES_CHANNEL,
            markets__object_id=sales_channel.pk,
            availability=Supplier.AVAILABLE,
        )

        supplier_market_availabilities = {
            supplier_market_availability.supplier.pk: supplier_market_availability.availability
            for supplier_market_availability
            in supplier_market_availabilities
        }

        supplier_articles = SupplierArticle.objects.filter(
            article__in=[cart_item.article for cart_item in cart_items],
            supplier_id__in=list(supplier_market_availabilities.keys()),
        )

        supplier_articles = {
            supplier_article.article_id: (supplier_article.supplier, supplier_article.stock)
            for supplier_article
            in supplier_articles.iterator()
        }

        items = []

        for cart_item in cart_items:
            availability = Supplier.AVAILABLE

            supplier, stock = supplier_articles.get(cart_item.article_id, (None, 0))

            supplier_sales_channel_article = SupplierSalesChannelArticle.objects.select_related(
                'supplier_article',
            ).filter(
                supplier_article__supplier=supplier,
                supplier_article__article_id=cart_item.article_id,
                sales_channel=sales_channel,
            ).last()

            if supplier_sales_channel_article is None:
                availability = Supplier.UNAVAILABLE
                unit_price = Decimal('0.00')
            else:
                unit_price = supplier_sales_channel_article.price

            item = Item(
                article=cart_item.article,
                unit_price=unit_price,
                quantity=cart_item.quantity,
                line_total=cart_item.quantity * unit_price,
                unavailable=availability == Supplier.UNAVAILABLE,
            )

            items.append(item)

        cart = cls(
            customer=customer,
            sales_channel=sales_channel,
            items=items,
            total=sum(item.line_total for item in items),
            can_continue_to_checkout=items and not any(item.unavailable for item in items),
        )

        return cart

    def add_item(self, article, quantity=1):
        item, created = CartItem.objects.get_or_create(
            customer=self.customer,
            sales_channel=self.sales_channel,
            article=article,
            defaults=dict(
                quantity=quantity,
            ),
        )

        if not created:
            item.quantity += quantity
            item.save(update_fields=('quantity',))

    def remove_item(self, article, quantity=None):
        items_with_article = CartItem.objects.filter(article=article)

        if quantity is None:
            items_with_article.update(quantity=0)
        else:
            while quantity:
                for cart_item in items_with_article.iterator():
                    quantity -= cart_item.quantity
