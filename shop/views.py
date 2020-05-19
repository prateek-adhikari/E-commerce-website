from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
from .forms import ContactForm
import json
# Create your views here.
def index(request): 
    allProds = []
    catprods = Product.objects.values('category')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil(n/4-n//4)
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {
        'allProds': allProds
    }
    return render(request, 'shop/index.html', params)
    
def product(request, pk):
    productView = Product.objects.get(pk=pk)
    context = {
        'product': productView
    }
    return render(request, 'shop/product.html', context)

def searchMatch(query, item):
    if query in item.product_name.lower() or query in item.product_description.lower() or query in item.category.lower() or query in item.sub_category.lower(): 
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n//4 + ceil(n/4-n//4)

        if len(prod)!=0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {
        'allProds': allProds,
        'msg': ''
    }
    if len(allProds) == 0 or len(query)<4:
        params = {
            'msg': 'No Products Found'
        }
    return render(request, 'shop/search.html', params)

def tracker(request):
    if request.method == "POST":
        orderid = request.POST.get('orderid')
        email = request.POST.get('email')
        try:
            order = Order.objects.filter(id=orderid,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderid)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc, 'time':item.timestamp})
                    response = json.dumps({'status':'success', 'updates':updates, 'itemsJson':order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "No Item"}')
        except:
            return HttpResponse('{"status": "Error"}')
    return render(request, 'shop/tracker.html')

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('items_json')
        camount = request.POST.get('amount')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        address2 = request.POST.get('address2')
        state = request.POST.get('state')
        city = request.POST.get('city') 
        zipcode = request.POST.get('zipcode')
        order = Order(items_json=items_json, camount=camount, fname=fname, lname=lname, email=email, phone=phone, address=address, address2=address2, state=state, city=city, zipcode=zipcode)
        order.save()
        update = OrderUpdate(order_id=order.id, update_desc="Your order has been placed")
        update.save()
        orderid = order.id
        thank = True
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': orderid})    
    return render(request, 'shop/checkout.html')

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            desc = form.cleaned_data.get('desc')
            contact = Contact(name=name, phone=phone, email=email, desc=desc)
            contact.save()
            return redirect('Home')
    else:
        form = ContactForm()
    return render(request, 'shop/contact.html', {'form': form})