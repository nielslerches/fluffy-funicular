from urllib.parse import urlencode

from django import forms
from django.core.paginator import Paginator
from django.views.generic import TemplateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from attributes.functions import get_all_attribute_sets, get_all_attributes
from catalog.models import Product, SalesChannel
from shared.functions import get_most_common_properties


class ViewWithNavItemsMixin:
    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data.update({
            'nav_items': [
                ('/', 'Shop'),
                *(
                    (reverse_lazy('shop:category') + '?' + urlencode({key: value}), value)
                    for key, value
                    in get_most_common_properties(
                        (
                            attribute_set
                            for identifier, attribute_set
                            in get_all_attribute_sets()
                        ),
                        maximum=4,
                    )
                )
            ],
        })

        return context_data


class IndexView(ViewWithNavItemsMixin, TemplateView):
    template_name = 'shop/index.html'


def merge_dict(a, b):
    a = a.copy()
    a.update(b)
    return a


class CategoryView(ViewWithNavItemsMixin, TemplateView):
    template_name = 'shop/category.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        attributes_config = get_all_attributes()

        search_arguments = {}

        for key in self.request.GET.keys():
            if key not in attributes_config:
                continue

            can_have_multiple_values = attributes_config[key]['multiple']
            if can_have_multiple_values:
                if key not in search_arguments:
                    search_arguments[key] = self.request.GET.getlist(key)
            else:
                search_arguments[key] = self.request.GET[key]

        choices = {}

        for key, config in sorted(attributes_config.items()):
            choices[key] = config.copy()
            choices[key]['default'] = search_arguments.get(key, [] if config['multiple'] else '')
            future_search_arguments = search_arguments.copy()
            future_search_arguments.update({key: choices[key]['default']})
            choices[key]['choices'] = [
                (
                    reverse_lazy('shop:category') + '?' + urlencode(merge_dict(search_arguments, {key: choice})),
                    choice
                )
                for choice
                in choices[key]['choices']
            ]

        objects = []

        for obj in Product.objects.prefetch_related('productimage_set').filter(deleted_at=None):

            for object_attribute_value in obj.attributes.filter(deleted_at=None):

                key = object_attribute_value.attribute_value.attribute.name
                value = object_attribute_value.attribute_value.name

                if key in search_arguments:

                    if isinstance(search_arguments[key], (tuple, list)):

                        if value not in search_arguments[key]:
                            break

                    else:

                        if search_arguments[key] != value:
                            break

                else:
                    continue

            else:
                objects.append(obj)

        paginator = Paginator(objects, int(self.request.GET.get('per-page', 20)))
        page = paginator.page(int(self.request.GET.get('page', 1)))

        context_data.update({
            'attributes_config': attributes_config,
            'search_arguments': search_arguments,
            'choices': choices,
            'paginator': paginator,
            'page': page,
        })

        return context_data


class ProductView(ViewWithNavItemsMixin, DetailView):
    template_name = 'shop/product.html'
    model = Product
    context_object_name = 'obj'

    def get_form_class(self):
        product = self.get_object()

        class AddItemToCart(forms.Form):
            article = forms.ModelChoiceField(product.article_set.all())
            quantity = forms.IntegerField(min_value=1)

        return AddItemToCart

    def get_form(self):
        form = self.get_form_class()
        if self.request.method == 'POST':
            form = form(self.request.POST)
        return form

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data.update({
            'form': self.get_form(),
        })

        return context_data

    def post(self, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            data = form.cleaned_data
            self.request.cart.add_item(
                data['article'],
                data['quantity'],
            )
            return redirect(reverse_lazy('shop:cart'))

        return redirect(self.get_object().get_absolute_url())


class CartView(ViewWithNavItemsMixin, TemplateView):
    template_name = 'shop/cart.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        sales_channel = SalesChannel.objects.get()

        context_data.update({
            'cart': self.request.cart,
        })

        return context_data
