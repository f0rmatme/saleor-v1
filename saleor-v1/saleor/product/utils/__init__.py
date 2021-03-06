from urllib.parse import urlencode

from django.conf import settings
from django.db import transaction
from django.db.models import F

from ...core.taxes import TaxedMoney, zero_taxed_money
from ...core.utils import get_paginator_items
from ...core.utils.filters import get_now_sorted_by
from ..tasks import update_products_minimal_variant_prices_task
from .availability import products_with_availability


def products_visible_to_user(user):
    # pylint: disable=cyclic-import
    from ..models import Product

    if user.is_authenticated and user.is_active and user.is_staff:
        return Product.objects.all()
    return Product.objects.published()


def products_with_details(user):
    products = products_visible_to_user(user)
    products = products.prefetch_related(
        "translations",
        "category__translations",
        "collections__translations",
        "images",
        "product_type__product_attributes__translations",
        "product_type__product_attributes__values__translations",
        "attributes__values__translations",
        "attributes__assignment__attribute__translations",
        "variants__variant_images__image",
        "variants__attributes__values__translations",
        "variants__attributes__assignment__attribute__translations",
    )
    return products


def products_for_products_list(user):
    products = products_visible_to_user(user)
    products = products.prefetch_related(
        "translations", "images", "variants__variant_images__image"
    )
    return products


def products_for_homepage(user, homepage_collection):
    products = products_visible_to_user(user)
    products = products.prefetch_related(
        "translations", "images", "variants__variant_images__image", "collections"
    )
    products = products.filter(collections=homepage_collection)
    return products


def get_product_images(product):
    """Return list of product images that will be placed in product gallery."""
    return list(product.images.all())


def products_for_checkout(user):
    products = products_visible_to_user(user)
    products = products.prefetch_related("variants__variant_images__image")
    return products


def get_variant_url_from_product(product, attributes):
    return "%s?%s" % (product.get_absolute_url(), urlencode(attributes))


def get_variant_url(variant):
    attributes = {
        str(attribute.pk): attribute
        for attribute in variant.product.product_type.variant_attributes.all()
    }
    return get_variant_url_from_product(variant.product, attributes)


def allocate_stock(variant, quantity):
    variant.quantity_allocated = F("quantity_allocated") + quantity
    variant.save(update_fields=["quantity_allocated"])


def deallocate_stock(variant, quantity):
    variant.quantity_allocated = F("quantity_allocated") - quantity
    variant.save(update_fields=["quantity_allocated"])


def decrease_stock(variant, quantity):
    variant.quantity = F("quantity") - quantity
    variant.quantity_allocated = F("quantity_allocated") - quantity
    variant.save(update_fields=["quantity", "quantity_allocated"])


def increase_stock(variant, quantity, allocate=False):
    """Return given quantity of product to a stock."""
    variant.quantity = F("quantity") + quantity
    update_fields = ["quantity"]
    if allocate:
        variant.quantity_allocated = F("quantity_allocated") + quantity
        update_fields.append("quantity_allocated")
    variant.save(update_fields=update_fields)


def get_product_list_context(request, filter_set):
    """Build a context from the given filter set.

    :param request: request object
    :param filter_set: filter set for product list
    :return: context dictionary
    """
    # Avoiding circular dependency
    from ..filters import SORT_BY_FIELDS

    qs = filter_set.qs
    if not filter_set.form.is_valid():
        qs = qs.none()
    products_paginated = get_paginator_items(
        qs, settings.PAGINATE_BY, request.GET.get("page")
    )
    products_and_availability = list(
        products_with_availability(
            products_paginated,
            request.discounts,
            request.country,
            request.currency,
            request.extensions,
        )
    )
    now_sorted_by = get_now_sorted_by(filter_set)
    arg_sort_by = request.GET.get("sort_by")
    is_descending = arg_sort_by.startswith("-") if arg_sort_by else False
    return {
        "filter_set": filter_set,
        "products": products_and_availability,
        "products_paginated": products_paginated,
        "sort_by_choices": SORT_BY_FIELDS,
        "now_sorted_by": now_sorted_by,
        "is_descending": is_descending,
    }


def collections_visible_to_user(user):
    # pylint: disable=cyclic-import
    from ..models import Collection

    if user.is_authenticated and user.is_active and user.is_staff:
        return Collection.objects.all()
    return Collection.objects.published()


def calculate_revenue_for_variant(variant, start_date):
    """Calculate total revenue generated by a product variant."""
    revenue = zero_taxed_money()
    for order_line in variant.order_lines.all():
        if order_line.order.created >= start_date:
            net = order_line.unit_price_net * order_line.quantity
            gross = order_line.unit_price_gross * order_line.quantity
            revenue += TaxedMoney(net, gross)
    return revenue


def collect_categories_tree_products(category):
    """Collect products from all levels in category tree."""
    products = category.products.all()
    descendants = category.get_descendants()
    for descendant in descendants:
        products = products | descendant.products.all()
    return products


@transaction.atomic
def delete_categories(categories_ids):
    """Delete categories and perform all necessary actions.

    Set products of deleted categories as unpublished, delete categories
    and update products minimal variant prices.
    """
    from ..models import Product, Category

    categories = Category.objects.select_for_update().filter(pk__in=categories_ids)
    categories.prefetch_related("products")

    products = Product.objects.none()
    for category in categories:
        products = products | collect_categories_tree_products(category)

    products.update(is_published=False, publication_date=None)
    product_ids = list(products.values_list("id", flat=True))
    categories.delete()
    update_products_minimal_variant_prices_task.delay(product_ids=product_ids)
