from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User, CatTest, Breeder, Transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import date, datetime
#from venmo_api import Client
#import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
#import regex


User = get_user_model()

# function to get venmo transactions and add any that are new to the db
def updateVenmo():    #this is not a view but is used in the login_page view
    access_token = Client.get_access_token(username='katz.breeder.system@gmail.com',
                                           password='K@tz_098')
    venmo = Client(access_token=access_token)
    my_id = (venmo.user.get_my_profile().id)
    transactions_list = venmo.user.get_user_transactions(user_id=my_id) # list of transactions from venmo

    for transaction in transactions_list:
        try:
            type = transaction.note.split(" ")[0]
        except IndexError:
            type = ''
        try:
            cat_name = transaction.note.split(" ")[2]
        except IndexError:
            cat_name = ''

        # Date is converted from timestamp to python datetime,date object
        try:
            formatted_date = date.fromtimestamp(transaction.date_completed)
        except TypeError:
            formatted_date = None
        #Try to create a valid object using the transaction id given by venmo. This determines if the transaction is already in the database
        try:
            valid_transaction = Transaction.objects.get(id=transaction.id)
            #If the transaction is not in the database already, create it
        except (Transaction.DoesNotExist):
            transaction = Transaction(id=transaction.id, cust_first_name=transaction.actor.first_name, cust_last_name=transaction.actor.last_name,
                                      cust_venmo_name=transaction.actor.username, amount=transaction.amount, type=type,
                                      cat_name=cat_name, date=formatted_date)
            transaction.save()

    #End the connection to venmo
    venmo.log_out(access_token)

# returns the http request for the main page: http://127.0.0.1:8000/
@login_required
def index(request):
    return render(request, "../templates/index.html")

# returns the http request for the "available kittens" page: http://127.0.0.1:8000/kittens/
@login_required
def kittens(request):
    cats = CatTest.objects.all()
    return render(request,"../templates/kittens.html", {'cats' : cats})

# returns the http request for the "register" page: http://127.0.0.1:8000/kittens/
def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        name = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        role = request.POST['role']
        cattery = request.POST['cattery']


        new_user = User.objects.create_user(name, email, password)
        new_user.first_name = firstname
        new_user.last_name = lastname
        new_user.role = role
        new_user.cattery = cattery
        new_user.save()
            #code for assigning the form data into the database fields.
        return redirect('login_page')
    return render(request, "../templates/register.html")

    def check_username(request):
        username = request.POST.get('username')

    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse('<div style="color: red"> This username already exists </div>')
    else:
        return HttpResponse('<div style="color: green"> This username is available </div>')
def login_page(request):

        if request.method == 'POST':
            username = request.POST['uname']
            password = request.POST['pw']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Updates the database with any new Venmo transactions
                #updateVenmo()
            return redirect('index')
            #else:
                #messages.error(request, 'Invalid form submission.')
                #return HttpResponse('Error, user does not exist')
        return render(request, "../templates/login_page.html")

def logoutuser(request):
    logout(request)
    return redirect('login_page')

    #returns the http request for the "available kittens" page: http://127.0.0.1:8000/kittens/

def cat_register(request):
    if request.method == 'POST' and request.FILES['image']:
        owner = request.user
        name = request.POST['catname']  
        gender = request.POST['gender']
        color = request.POST['color']
        personality = request.POST['personality']

        if not request.POST['mother']:
            mother = "Unknown"
        else:
            mother = request.POST['mother']

        if not request.POST['father']:
            father = "Unknown"
        else:
            father = request.POST['father']
        image = request.FILES['image']
        price = request.POST['price']
        bday = request.POST['bday']
        bday_date = datetime.strptime(bday, '%Y-%m-%d')
        cattest = CatTest(name=name, birthday=bday_date, gender=gender,
                  personality=personality, color=color, mother=mother, father=father, image=image, price=price, owner=owner)
        cattest.save()
        return redirect('kittens')
    #Fiter out the male and female cats
    females = CatTest.objects.filter(gender="Female")
    males = CatTest.objects.filter(gender="Male")
    return render(request, "../templates/cat_register.html", {'females':females, 'males':males})

def query_test(request):
    transactions = Transaction.objects.all()
    transaction_output_list = []
    cat_name_input = request.POST.get('catname', False)
    month_year_input = request.POST.get('monthyear', False)
    cust_name_input = request.POST.get('custname', False)

    if cust_name_input != False:
        cust_name_list = Transaction.objects.filter(cust_last_name=cust_name_input)
        for each in cust_name_list:
            date = each.date.strftime("%B %d %Y")
            trans_string = "%s %s paid $ %s on %s for %s" % (each.cust_first_name, each.cust_last_name, each.amount, date, each.catID)
            transaction_output_list.append(trans_string)

    if cat_name_input != False:
        cat_name_list = Transaction.objects.filter(cat_name=cat_name_input)
        for each in cat_name_list:
            date = each.date.strftime("%B %d %Y")
            trans_string = "%s %s paid $ %s on %s for %s" % (each.cust_first_name, each.cust_last_name, each.amount, date, each.cat_name)
            transaction_output_list.append(trans_string)

    '''
    if month_year_input != False:
        month_year_list = Transaction.objects.()
        print(month_year_input)
        for each in month_year_list:
            match = regex.search(month_year_input + d, each.date)
            for each in match:
                date = each.date.strftime("%B %d %Y")
                trans_string = "%s %s paid $ %s on %s for %s" % (each.cust_first_name, each.cust_last_name, each.amount, date, each.catID)
                transaction_output_list.append(trans_string)
    '''

    #If no info is given on the form
    if cat_name_input == False and month_year_input == False and cust_name_input == False:
        for each in transactions:
            date = each.date.strftime("%B %d %Y")
            trans_string = "%s %s paid $ %s on %s for %s" % (each.cust_first_name, each.cust_last_name, each.amount, date, each.cat_name)
            transaction_output_list.append(trans_string)
    return render(request, "../templates/query_test.html", {'transactions':transaction_output_list})

def about(request):
    return render(request, "../templates/about.html")

def kittens_purchase(request, id, id2):
    catguy = CatTest.objects.get(id=id)
    buyer = User.objects.get(id=id2)
    if catguy.status == 'Reserved':
        catguy.status = 'Purchased'
    else:
        catguy.status = 'Reserved'
        catguy.buyer = buyer.username
    catguy.save()
    cats = CatTest.objects.all()

    return redirect('kittens')
    return render(request,"../templates/kittens.html", {'cats' : cats})