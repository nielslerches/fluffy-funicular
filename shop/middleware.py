from catalog.models import SalesChannel

from shop.functions import Cart
from shop.models import Customer


def get_or_create_customer_middleware(get_response):
    def middleware(request):

        customer_id = request.session.get('customer_id')
        customer = Customer.objects.filter(pk=customer_id).first()

        if not customer:
            customer = Customer.objects.create()
            customer_id = customer.pk
            request.session['customer_id'] = customer_id

        request.cart = Cart.get(customer, SalesChannel.objects.get())

        response = get_response(request)

        return response

    return middleware
