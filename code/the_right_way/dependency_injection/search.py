# Our (pretend) product search API module


from shop.models import Product


class Filter:
    NAME = 'name'
    COLOR = 'color'


PAGE_SIZE = 5


# To have an implementation we can test against, we actually just use QuerySets
# here, but in a real project we might be using something not QuerySet based
# e.g. external HTTP API or ElasticSearch or something

def special_product_search(filters, special_offer, *, page=1):
    return _search(filters, special_offer.get_products(), page=page)


def product_search(filters, *, page=1):
    return _search(filters, Product.objects.all(), page=page)


def _search(filters, products, *, page=1):
    if Filter.NAME in filters:
        products = products.filter(name__icontains=filters[Filter.NAME])
    if Filter.COLOR in filters:
        products = products.filter(colors__name__icontains=filters[Filter.COLOR])

    # paging
    start = (page - 1) * PAGE_SIZE
    products = list(products.order_by('name')[start:start + PAGE_SIZE])
    return products
