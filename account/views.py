from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import inlineformset_factory


def home(request):
    # return HttpResponse('Home Page')
    order = Order.objects.all()
    customer = Customer.objects.all()

    total_order = order.count()
    orders_delivered = order.filter(status='Delivered').count()
    orders_pending = order.filter(status='Pending').count()

    context={'order':order,
    'customer':customer,
    'total_order':total_order,
    'orders_delivered':orders_delivered,
    'orders_pending':orders_pending
    }
    return render(request,'account/dashboard.html',context)

def product(request):
    # return HttpResponse('Product Page')
    product = Product.objects.all()
    context = {'product':product}
    return render(request,'account/product.html',context)

def customer(request,pk):
    # return HttpResponse('Customer Page')
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()
    total_order =  order.count()

    context={'order':order,
    'customer':customer,
    'product':product,
    'total_order':total_order}
    return render(request,'account/customer.html',context)

# def createOrder(request,pk):
#     customer = Customer.objects.get(id=pk)
#     form = OrderForm(initial={'customer':customer})
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')

#     context= {'form':form}
#     return render(request,'account/order_form.html',context)

def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields = ('product','status'))
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context= {'formset':formset}
    return render(request,'account/order_form.html',context)


def updateOrder(request,pk): 
    order = Order.objects.get(id=pk)  #Creating a form to change an existing
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context= {'form':form}
    return render(request,'account/order_form.html',context)

def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order':order}
    return render(request,'account/delete.html',context)