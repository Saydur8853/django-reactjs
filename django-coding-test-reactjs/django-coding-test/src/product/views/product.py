from django.views import generic
from datetime import datetime
from django.shortcuts import render
from product.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class CreateProductView(generic.TemplateView):
    template_name = "products/create.html"

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values("id", "title")
        context["product"] = True
        context["variants"] = list(variants.all())
        return context


class ProductListview(generic.ListView):
    template_name = "products/list.html"
    model = Product
    context_object_name = "products"
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get filter parameters from GET request
        title = self.request.GET.get("title")
        variant = self.request.GET.get("variant")
        price_from = self.request.GET.get("price_from")
        price_to = self.request.GET.get("price_to")
        date = self.request.GET.get("date")

        # Apply filters to queryset
        if title:
            queryset = queryset.filter(title__icontains=title)
        if variant:
            queryset = queryset.filter(variants__variant_title=variant)
        if price_from and price_to:
            queryset = queryset.filter(prices__price__range=(price_from, price_to))
        if date:
            queryset = queryset.filter(created_at__date=date)

        return queryset.distinct()


def product_list(request):
    variant_data = Variant.objects.all()
    product_variant = ProductVariant.objects.all()
    product_data = Product.objects.all()
    title = request.GET.get("title")
    variant = request.GET.get("variant")
    price_from = request.GET.get("price_from")
    price_to = request.GET.get("price_to")
    date = request.GET.get("date")

    # Apply filters to queryset
    if title:
        product_data = product_data.filter(title__icontains=title)
    if variant:
        product_data = product_data.filter(variants__variant_title=variant)
    if price_from and price_to:
        product_data = product_data.filter(prices__price__range=(price_from, price_to))
    if date:
        product_data = product_data.filter(created_at__date=date)

    page = request.GET.get("page", 1)
    paginator = Paginator(product_data, 2)

    try:
        product_data = paginator.page(page)
    except PageNotAnInteger:
        product_data = paginator.page(1)
    except EmptyPage:
        product_data = paginator.page(paginator.num_pages)

    context = {
        "products": product_data,
        "variants": variant_data,
        "product_variant": product_variant,
    }
    return render(request, "products/list.html", context)
    # listing_filter =

    # def get(self, request):
    #     title = request.GET.get("title", "")
    #     variant_id = request.GET.get("variant", "")
    #     price_from = request.GET.get("price_from", "")
    #     price_to = request.GET.get("price_to", "")
    #     date = request.GET.get("date", "")

    #     products = Product.objects.all()

    #     # Filter by product title
    #     if title:
    #         products = products.filter(title__icontains=title)

    #     # Filter by variant
    #     if variant_id:
    #         products = products.filter(variants__variant_id=variant_id)

    #     # Filter by price range
    #     if price_from and price_to:
    #         products = products.filter(prices__price__range=(price_from, price_to))

    #     # Filter by date
    #     if date:
    #         date = datetime.strptime(date, "%Y-%m-%d").date()
    #         products = products.filter(created_at__date=date)

    #     return render(request, "products.html", {"products": products})


# from django.views import View
# from django.shortcuts import render
# from datetime import datetime

# # from .models import Product, ProductVariantPrice


# class FilterProductsView(View):
#     def get(self, request):
#         title = request.GET.get("title", "")
#         variant_id = request.GET.get("variant", "")
#         price_from = request.GET.get("price_from", "")
#         price_to = request.GET.get("price_to", "")
#         date = request.GET.get("date", "")

#         products = Product.objects.all()

#         # Filter by product title
#         if title:
#             products = products.filter(title__icontains=title)

#         # Filter by variant
#         if variant_id:
#             products = products.filter(variants__variant_id=variant_id)

#         # Filter by price range
#         if price_from and price_to:
#             products = products.filter(prices__price__range=(price_from, price_to))

#         # Filter by date
#         if date:
#             date = datetime.strptime(date, "%Y-%m-%d").date()
#             products = products.filter(created_at__date=date)

#         return render(request, "list.html", {"products": products})
