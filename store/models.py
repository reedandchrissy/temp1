from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField




# Create your models here.

class TimeSet(models.Model):
	End_time = models.DateTimeField(max_length=100, null=True)
	Delivery_date = models.DateField(max_length=100, null=True)

class WebsiteReport(models.Model):
	name = models.CharField(max_length=100, null=True)
	period = models.CharField(max_length=100, null=True)
	content = models.TextField(null=True)


class FarmReport(models.Model):
	name = models.CharField(max_length=100, null=True)
	period = models.CharField(max_length=100, null=True)
	content = models.TextField(null=True)


class OverallReport(models.Model):
	name = models.CharField(max_length=100, null=True)
	period = models.CharField(max_length=100, null=True)
	content = models.TextField(null=True)

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)
    phone = PhoneNumberField()
    profile_pic = models.ImageField(default='touxiang.jpg', null=True, blank=True)


    def __str__(self):
        return self.name




class Product(models.Model):
	CATEGORY = (
		('Vegetables', 'Vegetables'),
		('Fruits', 'Fruits'),
		('Eggs', 'Eggs'),
	)
	name = models.CharField(max_length=200)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	price = models.FloatField()
	describe = models.CharField(max_length=1000)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url


class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(max_length=100, null=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)
	delivered = models.BooleanField(default=False)
	delivered_date = models.DateField(max_length=100, null=True,blank=True)


	def __str__(self):
		return str(self.id)

	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			shipping = True
		return shipping



	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total



class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order,  on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)




	def __str__(self):
		return self.product.name

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)


	def __str__(self):
		return self.address


class Comment(models.Model):
    name = models.CharField(max_length=200, null=True)
    content = models.TextField(help_text='write your comment')


class ReturnManagement(models.Model):
	CATEGORY = (
		('GetRefund', 'GetRefund'),
		('ResendItem', 'ResendItem'),
	)
	item_name = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	total_value = models.FloatField()
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	date = models.DateField(max_length=100, null=True)
	note = models.CharField(max_length=200, null=True, blank=True)



