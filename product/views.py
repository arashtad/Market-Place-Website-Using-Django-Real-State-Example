from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductSearchForm, GeneralSearchForm, PriceRangeFilterForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})

def home(request):
    form = GeneralSearchForm(request.GET)
    
    if request.method == 'GET' and 'search' in request.GET:
        # The 'search' parameter is present in the query string, indicating a search request.
        if form.is_valid():
            search_request = request.GET.urlencode()
            search_keyword = search_request.split('=')[1].replace('+',' ')
            search_keyword = search_keyword.replace('%2C',',')
            products = Product.objects.all()

            zip_code_list = list(products.filter(zip_code=search_keyword))
            city_list = list(products.filter(city__icontains=search_keyword))
            address_list = list(products.filter(address__icontains=search_keyword))

            query_params = ''
            if (len(zip_code_list) != 0):
                query_params = f'zip_code={zip_code_list[0].zip_code}&city=&address='
            elif (len(city_list) != 0):
                query_params = f'zip_code=&city={city_list[0].city}&address='
            elif (len(address_list) != 0):
                query_params = f'zip_code=&city=&address={address_list[0].address}'
            return redirect(f'/products/?{query_params}')

    return render(request, 'home.html', {'form': form})
            

def product_list(request):
    form = ProductSearchForm(request.GET)
    price_filter_form = PriceRangeFilterForm(request.GET)
    products = Product.objects.all()

    if price_filter_form.is_valid():
        min_price = price_filter_form.cleaned_data.get('min_price')
        max_price = price_filter_form.cleaned_data.get('max_price')

        if min_price is not None:
            products = products.filter(price__gte=min_price)
        if max_price is not None:
            products = products.filter(price__lte=max_price)

    if form.is_valid():
        zip_code = form.cleaned_data.get('zip_code')
        city = form.cleaned_data.get('city')
        address = form.cleaned_data.get('address')

        if zip_code:
            products = products.filter(zip_code=zip_code)
        if city:
            products = products.filter(city__icontains=city)
        if address:
            products = products.filter(address__icontains=address)
    
    return render(request, 'product_list.html', {'products': products, 'form': form})
