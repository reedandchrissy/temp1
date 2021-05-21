from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group

from django.contrib.auth.models import User




# Create your views here.
from .models import *
from .forms import OrderItemForm, CreateUserForm, CustomerForm, CommentForm, OrderForm, ReturnItemForm
from .filters import ProductFilter, OrderFilter, OrderMatchFilter, DeliveryFilter
from .decorators import unauthenticated_user, allowed_users, admin_only




def home(request):
	context = {}
	return render(request, 'store/home.html', context)


@login_required(login_url='login')
@admin_only
def homein(request):


	context = {}
	return render(request, 'store/homein.html', context)


def store(request):
   times = TimeSet.objects.get(id=1)
   delivery = times.Delivery_date
   end_time = times.End_time

   products = Product.objects.all()

   myFilter = ProductFilter(request.GET, queryset=products)
   products = myFilter.qs

   context = {'times': times, 'delivery': delivery, 'end_time': end_time, 'products': products, 'myFilter': myFilter}
   return render(request, 'store/store.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',  'customer'])
def storein(request):
	times = TimeSet.objects.get(id=1)
	delivery = times.Delivery_date
	end_time = times.End_time

	products = Product.objects.all()

	myFilter = ProductFilter(request.GET, queryset=products)
	products = myFilter.qs

	context = {'times': times, 'delivery': delivery, 'end_time': end_time, 'products': products, 'myFilter': myFilter}
	return render(request, 'store/storein.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
		cartItems = order['get_cart_items']

	context = {'items': items, 'order': order, 'cartItems': cartItems}

	return render(request, 'store/cart.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
		cartItems = order['get_cart_items']

	context = {'items': items, 'order': order, 'cartItems': cartItems}

	return render(request, 'store/checkout.html', context)


def comments(request):
	comments = Comment.objects.all()

	context = {'comments': comments}
	return render(request, 'store/comments.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def commentsin(request):
	comments = Comment.objects.all()

	context = {'comments': comments}

	return render(request, 'store/commentsin.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def writeComment(request):
	form = CommentForm()
	if request.method == 'POST':
		# print('Printing POST:', request.POST)
		form = CommentForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/commentsin/')

	context = {'form': form}
	return render(request, 'store/write_comment.html', context)



def contact(request):
	context = {}
	return render(request, 'store/contact.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',  'customer'])
def contactin(request):

	context = {}
	return render(request, 'store/contactin.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
	orders = request.user.customer.order_set.all()

	print('ORDERS:', orders)



	context = {'orders': orders}

	return render(request, 'store/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def customersetting(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()

	context = {'form': form, 'customer': customer}

	return render(request, 'store/customer_setting.html', context)










@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def order(request, pk_test):
	order = Order.objects.get(id=pk_test)

	items = order.orderitem_set.all()

	ads = order.shippingaddress_set.all()

	context = {'order': order, 'items': items, 'ads': ads}
	return render(request, 'store/order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def receipt(request, pk_test):
	order = Order.objects.get(id=pk_test)

	items = order.orderitem_set.all()

	ads = order.shippingaddress_set.all()

	context = {'order': order, 'items': items, 'ads': ads}
	return render(request, 'store/receipt.html', context)



@unauthenticated_user
def loginpage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('homein')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'store/login.html', context)

def logoutuser(request):
    logout(request)
    return redirect('home')


@unauthenticated_user
def register(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)
			Customer.objects.create(
				user=user,
				name=user.username,
			)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')

	context = {'form': form}
	return render(request, 'store/register.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def dashboard(request):

	items = OrderItem.objects.select_related('product', 'order')

	myFilter1 = OrderFilter(request.GET, queryset=items)
	items = myFilter1.qs

	orders = Order.objects.all()

	myFilter = OrderMatchFilter(request.GET, queryset=orders)
	orders = myFilter.qs


	context = { 'items': items, 'myFilter1': myFilter1, 'orders': orders, 'myFilter': myFilter}

	return render(request, 'store/dashboard.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customerInfo(request):
	customers = Customer.objects.all()

	context = {'customers': customers}

	return render(request, 'store/customer_info.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def reports(request):
	context = {}
	return render(request, 'store/reports.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delivery(request):

	ads = ShippingAddress.objects.select_related('order','customer')

	myFilter = DeliveryFilter(request.GET, queryset=ads)
	ads = myFilter.qs


	context = {'ads': ads,  'myFilter': myFilter }
	return render(request, 'store/delivery.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateorder(request, pk):

	orderitem = OrderItem.objects.get(id=pk)

	form = OrderItemForm(instance=orderitem)

	if request.method == 'POST':
		form = OrderItemForm(request.POST, instance=orderitem)
		if form.is_valid():
			form.save()
			return redirect('/dashboard/')

	context = {'form': form}
	return render(request, 'store/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def status(request, pk):

	order = Order.objects.get(id=pk)

	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/dashboard/')

	context = {'form': form}
	return render(request, 'store/status.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteorder(request, pk):
    orderitem = OrderItem.objects.get(id=pk)
    if request.method == "POST":
        orderitem.delete()
        return redirect('/dashboard/')

    context = {'item': orderitem}
    return render(request, 'store/delete.html', context)





@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)



def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	date_ordered = datetime.datetime.now()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer

		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id
		order.date_ordered = date_ordered



		if total == order.get_cart_total:
			order.complete = True
		order.save()


		if order.shipping == True:
			ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
	else:
		print('User is not logged in')

	return JsonResponse('Payment submitted..', safe=False)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def reports(request):
	websitereports = WebsiteReport.objects.all()

	farmreports = FarmReport.objects.all()
	overallreports = OverallReport.objects.all()

	context = {'websitereports': websitereports, 'farmreports': farmreports, 'overallreports': overallreports}

	return render(request, 'store/reports.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def websiteReport(request, pk):
	websitereport = WebsiteReport.objects.get(id=pk)

	context = {'websitereport': websitereport}
	return render(request, 'store/website_report.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def farmReport(request, pk):
	farmreport = FarmReport.objects.get(id=pk)

	context = {'farmreport': farmreport}
	return render(request, 'store/farm_report.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def overallReport(request, pk):
	overallreport = OverallReport.objects.get(id=pk)

	context = {'overallreport': overallreport}
	return render(request, 'store/overall_report.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def Return(request):

	returnitem = ReturnManagement.objects.all()

	context = {'returnitem': returnitem}
	return render(request, 'store/ReturnManagement.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def enterItem(request):
	form = ReturnItemForm()
	if request.method == 'POST':
		# print('Printing POST:', request.POST)
		form = ReturnItemForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/ReturnManagement/')

	context = {'form': form}
	return render(request, 'store/enter_return_item.html', context)

