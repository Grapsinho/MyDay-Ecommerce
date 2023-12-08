from django.shortcuts import render, redirect
from inventory.models import *
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.conf import settings
from datetime import datetime, timedelta

import json

# Create your views here.
# @cache_page(60 * 15)
def home(request):
    cat = Category.objects.all()

    q = request.GET.get('search') if request.GET.get('search') != None else ''

    if q == '':
        product = ''
    else:
        product = ProductInventory.objects.filter(product__name__icontains=q, is_active=True)

    context = {"cat": cat, 'product': product, "q": q}
        
    return render(request, 'mainApp/home.html', context=context)

@cache_page(60 * 15)
def collections(request, slug):
    product_data = ProductInventory.objects.filter(product__category__slug=slug, is_active=True).values('attribute_values__attribute_value', "attribute_values__product_attribute__name", "product__category__name").distinct()

    # Create a dictionary to store the reorganized data
    reorganized_data = {}

    # Iterate through the query results
    for data in product_data:
        attribute_name = data["attribute_values__product_attribute__name"]
        attribute_value = data["attribute_values__attribute_value"]
        
        # Check if the attribute name already exists in the reorganized data
        if attribute_name in reorganized_data:
            # If it exists, append the value to the existing list
            reorganized_data[attribute_name].append(attribute_value)
        else:
            # If it doesn't exist, create a new list with the value
            reorganized_data[attribute_name] = [attribute_value]

    # Now, reorganized_data contains the attributes and their corresponding values grouped together.
    # You can access them like this:
    # for attribute, values in reorganized_data.items():
    #     print(f"{attribute}: {', '.join(values)}")

    cat = Category.objects.all()

    cat_name = ''

    for i in product_data:
        cat_name = i['product__category__name']

    context = {"cat": cat, "rec_data": reorganized_data.items(), "cat_name": cat_name}
        
    return render(request, 'mainApp/collections.html', context=context)

def product_detail(request, slug):
    product = ProductInventory.objects.filter(product__slug=slug, is_active=True)

    opr = product.values("attribute_values__attribute_value", "attribute_values__product_attribute__name").distinct()

    produ_name = ''

    for i in product:
        produ_name = i.product.name
    
    reorganized_data = {}

    for i in opr:
        attribute_name = i["attribute_values__product_attribute__name"]
        attribute_value = i["attribute_values__attribute_value"]
        
        # Check if the attribute name already exists in the reorganized data
        if attribute_name in reorganized_data:
            # If it exists, append the value to the existing list
            reorganized_data[attribute_name].append(attribute_value)
        else:
            # If it doesn't exist, create a new list with the value
            reorganized_data[attribute_name] = [attribute_value]

    cat = Category.objects.all()

    context = {"product": product,"rec_data": reorganized_data.items(), "cat": cat, "produ_name": produ_name}
        
    return render(request, 'mainApp/product_detail.html', context=context)

def cart(request):
    cat = Category.objects.all()

    cart_items = request.COOKIES.get('cart_items')

    if cart_items:
        cart_items = eval(cart_items)  # Convert the string back to a list

        total_price = 0
        cart_products = []

        for cart_item in cart_items:
            product = ProductInventory.objects.get(sku=cart_item['sku'])
            price = product.retail_price * cart_item['quantity']
            total_price += price

            # Create a dictionary to store the reorganized data
            reorganized_data = {}

            # Iterate through the query results
            for data in product.attribute_values.all():
                
                # Check if the attribute name already exists in the reorganized data
                if data.product_attribute in reorganized_data:
                    # If it exists, append the value to the existing list
                    reorganized_data[data.product_attribute].append(data.attribute_value)
                else:
                    # If it doesn't exist, create a new list with the value
                    reorganized_data[data.product_attribute] = [data.attribute_value]

            color = []
            sizes = []

            for attr, cool in reorganized_data.items():
                if attr.name == 'Color':
                    color.append(cool[0])
                elif attr.name == 'Size':
                    sizes.append(cool[0])
            
            cart_products.append({
                'name': product.product.name,
                'img_url': str(product.media.get(product_inventory=product).img_url),
                'quantity': cart_item['quantity'],
                'fullPrice': price,
                'price': product.retail_price,
                'sku': product.sku,
                "stock": Stock.objects.get(product_inventory=product).units,
                "color": color[0],
                "sizes": sizes[0]
            })

        context = {"cat": cat, "cart_products": cart_products}
    
    else:
        context = {"cat": cat}

    return render(request, 'mainApp/cart.html', context=context)

def checkout(request):
    cart_items = request.COOKIES.get('cart_items')

    if cart_items:
        cart_items = eval(cart_items)  # Convert the string back to a list

        total_price = 0
        cart_products = []

        for cart_item in cart_items:
            product = ProductInventory.objects.get(sku=cart_item['sku'])
            price = product.retail_price * cart_item['quantity']
            total_price += price

            # Create a dictionary to store the reorganized data
            reorganized_data = {}

            # Iterate through the query results
            for data in product.attribute_values.all():
                
                # Check if the attribute name already exists in the reorganized data
                if data.product_attribute in reorganized_data:
                    # If it exists, append the value to the existing list
                    reorganized_data[data.product_attribute].append(data.attribute_value)
                else:
                    # If it doesn't exist, create a new list with the value
                    reorganized_data[data.product_attribute] = [data.attribute_value]

            color = []
            sizes = []

            for attr, cool in reorganized_data.items():
                if attr.name == 'Color':
                    color.append(cool[0])
                elif attr.name == 'Size':
                    sizes.append(cool[0])
            
            cart_products.append({
                'name': product.product.name,
                'img_url': str(product.media.get(product_inventory=product).img_url),
                'quantity': cart_item['quantity'],
                'fullPrice': price,
                'price': product.retail_price,
                'sku': product.sku,
                "stock": Stock.objects.get(product_inventory=product).units,
                "color": color[0],
                "sizes": sizes[0]
            })

        context = {"cart_products": cart_products}

        return render(request, 'mainApp/checkout.html', context=context)
    
    else:
        return render(request, 'mainApp/checkout.html')

def processOrder(request):
    transaction_id = datetime.now().timestamp()
    cart_items = request.COOKIES.get('cart_items')

    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        number = request.POST.get('number')
        lastName = request.POST.get('lastName')
        city = request.POST.get('city')
        postalCode = request.POST.get('postalCode')
        address = request.POST.get('address')


        costumer, created = Costumer.objects.get_or_create(email=email)

        costumer.name = name
        costumer.save()
            
        order = Order.objects.create(
            costumer=costumer,
            complete=False,
        )

        if cart_items:
            cart_items = eval(cart_items)  # Convert the string back to a list
            total_price = 0
            for cart_item in cart_items:
                product = ProductInventory.objects.get(sku=cart_item['sku'])

                orderItem = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=cart_item['quantity'],
                )

                price = product.retail_price * cart_item['quantity']
                total_price += price

                stock_item = Stock.objects.get(product_inventory__sku=cart_item['sku'])

                # Update stock attributes
                stock_item.units -= cart_item['quantity']  # Reduce available units
                stock_item.units_sold += cart_item['quantity']  # Increase units sold

                # Save the updated stock information
                stock_item.save()


            #ანუ ვინც არ უნდა ყიდულობდეს მაინც გვინდა რომ გვქონდეს ეს მნიშვნელობები
            total321 = total_price + 5
            total4321 = float(order.get_all_total) + 5

            order.transaction_id = transaction_id

            if float(total321) == total4321:
                print('rame')
                order.complete = True
            order.save()
            
            ShippingAddress.objects.create(
                costumer=costumer,
                order=order,
                address=address,
                city=city,
                Postal_code=postalCode,
                name=name,
                last_name=lastName,
                phone_number=number,
                email=email
            )

            response = HttpResponse('Success')
            response.delete_cookie('cart_items')

            return response

# @cache_page(60 * 15)
def filter_products(request):
    sort_option = request.GET.get('sort', 'low_to_high')
    product_name = request.GET.get('product_name')

    if sort_option == 'low_to_high':
        products = ProductInventory.objects.filter(product__name__icontains=product_name, is_active=True).order_by('retail_price')
    elif sort_option == 'high_to_low':
        products = ProductInventory.objects.filter(product__name__icontains=product_name, is_active=True).order_by('-retail_price')

    
    
    serialized_products = [{'name': product.product.name, 'price': product.retail_price, 'slug': product.product.slug} for product in products]



    return JsonResponse({'products': serialized_products})

def filter_products_for_collections(request):
    sort_option = request.GET.get('sort', 'low_to_high')
    product_name = request.GET.get('product_name')
    filters = request.GET.get('filters')

    if filters: 
        filters_dict = json.loads(filters)

    if sort_option == 'low_to_high':
        
        if filters_dict: 
            products = ProductInventory.objects.filter(product__category__slug__icontains=product_name, attribute_values__attribute_value__in=filters_dict, is_active=True).order_by('retail_price').distinct()

        else:
            products = ProductInventory.objects.filter(product__category__slug__icontains=product_name, is_active=True).order_by('retail_price').distinct()

    elif sort_option == 'high_to_low':
        
        if filters_dict: 
            products = ProductInventory.objects.filter(product__category__slug__icontains=product_name, attribute_values__attribute_value__in=filters_dict, is_active=True).order_by('-retail_price').distinct()
                
        else:
            products = ProductInventory.objects.filter(product__category__slug__icontains=product_name, is_active=True).order_by('-retail_price').distinct()
                
        

    serialized_products = [{
        'name': product.product.name,
        'price': product.retail_price,
        'slug': product.product.slug,
        'img_url': str(Media.objects.get(product_inventory=product).img_url)} for product in products]


    return JsonResponse({'products': serialized_products})

def filter_products_for_productDtl(request):
    product_name = request.GET.get('product_name')
    filters = request.GET.get('filters')

    l2 = []


    if filters: 

        filters_dict = json.loads(filters)

        for i in filters_dict:  
            l2.append(i['value'])

        if filters_dict: 
            if len(l2) == 2:
                l2.pop(0)  

            products = ProductInventory.objects.get(product__name__icontains=product_name, attribute_values__attribute_value__in=l2, is_active=True)
                        
        else:
            products = ProductInventory.objects.get(product__name__icontains=product_name, is_default=True, is_active=True)

        
    l1 = list()
   
    for ii in products.attribute_values.all():
        l1.append(ii.attribute_value)

    try:
        try:
            rem = products.media.get(product_inventory = products)
            img_url = rem.img_url.url if rem.img_url else None 

            serialized_products = {'name': products.product.name,'code': products.sku,'desc': products.product.description, 'price': products.retail_price, 'slug': products.product.slug, 'img_url': img_url, 'stock': str(Stock.objects.get(product_inventory=products).units),}
        except:
            rem = products.media.filter(product_inventory = products)
            img_url = '/static/images/No Image.svg'
            for i in range(len(rem)):
                if rem[i]:
                    img_url = rem[i].img_url.url if rem[i].img_url else None 
                else:
                    img_url = '/static/images/No Image.svg'
                
            
            serialized_products = {'name': products.product.name,'code': products.sku,'desc': products.product.description, 'price': products.retail_price, 'slug': products.product.slug, 'img_url': img_url,}

    except Media.DoesNotExist:
        serialized_products = {'name': products.product.name,'code': products.sku,'desc': products.product.description, 'price': products.retail_price, 'slug': products.product.slug,}
        print('no')

    return JsonResponse({'products': serialized_products, "values": l1})

def add_to_cart(request):

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        sku = request.POST.get('sku')

        l1 = list()

        l1.append(quantity)

        # Initialize an empty list to store cart items
        cart_items = request.COOKIES.get('cart_items')
        if cart_items:
            cart_items = eval(cart_items)  # Convert the string back to a list
        else:
            cart_items = []

        # Check if the product is already in the cart
        product_index = None
        for index, item in enumerate(cart_items):
            if item['sku'] == sku:
                product_index = index
                break
            
        # Set the expiration time to 1 day from now
        expiration_time = datetime.now() + timedelta(days=1)    

        # If the product is in the cart, update the quantity
        if product_index is not None:
            response = JsonResponse({'message': 'already in cart'})
            return response
        else:
            # Add a new item to the cart
            cart_items.append({'sku': sku, 'quantity': quantity})
        
            product = ProductInventory.objects.get(sku=sku)

            # Set the updated cart data in cookies
            response = JsonResponse({"price": product.retail_price * quantity, "sku": product.sku, 'quantity': quantity, "name": product.product.name, "img_url": str(product.media.get(product_inventory=product).img_url)})
            response.set_cookie('cart_items', cart_items, expires=expiration_time)
            return response
    else:
        return JsonResponse({'message': 'Invalid request'})

def get_cart_data(request):
    cart_items = request.COOKIES.get('cart_items')
    
    if cart_items:
        cart_items = eval(cart_items)  # Convert the string back to a list

        total_price = 0
        cart_products = []

        for cart_item in cart_items:
            product = ProductInventory.objects.get(sku=cart_item['sku'])
            price = product.retail_price * cart_item['quantity']
            total_price += price
            
            cart_products.append({
                'name': product.product.name,
                'img_url': str(product.media.get(product_inventory=product).img_url),
                'quantity': cart_item['quantity'],
                'price': price,
                'sku': product.sku,
                "stock": Stock.objects.get(product_inventory=product).units
            })

        return JsonResponse({'total_price': total_price, 'cart_products': cart_products})
    
    else:
        return JsonResponse({'message': 'Cart is empty'})

def updateCart(request):
    cart_items = request.COOKIES.get('cart_items')

    if request.method == 'POST':
        action = request.POST.get('action')
        sku = request.POST.get('sku')  # Assuming the SKU is sent along with the action

        cart_items = eval(cart_items)
        # Find the item in the cart_items list
        for cart_item in cart_items:

            if cart_item['sku'] == sku:
                if action == 'add':
                    cart_item['quantity'] += 1
                elif action == 'remove':
                    cart_item['quantity'] -= 1

                # Handle quantity less than or equal to zero
                if cart_item['quantity'] <= 0:
                    cart_items.remove(cart_item)

    response = JsonResponse({"success": True})  # Create a JsonResponse object
    response.set_cookie('cart_items', cart_items)  # Set the cookie with updated cart_items
    return response 