import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from datetime import timedelta, datetime

# Create your views here.
def index(request):
    all_rows = Deceased_Info.objects.all().order_by('-id')

    organized_cases = []


    for person in all_rows:
        events = Events.objects.filter(event_deceased_info=person)

        case_dict = {}

        case_dict["person"] = person
        case_dict["events"] = get_eventlist(events)

        organized_cases.append(case_dict)


    return render(request, "myapp/index.html", {
        "organized_cases":organized_cases,
        "all_rows":all_rows
    })


def get_eventlist(events):

    updated_events = []

    for event in events:
        event_dict= {}
        duration = event.duration
        start_time = event.time
        start_date = event.date
        start_dt = datetime.combine(start_date, start_time)

        delta = timedelta(hours=duration)

        end_time = start_dt + delta

        event_dict["event_title"] = event.event_title
        event_dict["event_location"] = event.event_location
        event_dict["date"] = event.date
        event_dict["time"] = event.time
        event_dict["duration"] = event.duration
        event_dict["end_time"] = end_time
        event_dict["id"] = event.id

        print(start_dt)
  

        updated_events.append(event_dict)

    return(updated_events)



   
# def get_endtime(start_date, start_time, dur):
#         start_dt = datetime.combine(start_date, start_time)
#         delta = timedelta(hours=dur)
#         end_time = start_dt + delta
#         return(end_time)
#         # does this function have potential to do more? like create the dictionary too?


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "myapp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "myapp/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "myapp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "myapp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "myapp/register.html")
    

def add_case(request):
    if request.method == "GET":
        return render(request, 'myapp/add_case.html')
    
    elif request.method == "POST":

        new_full_name = request.POST['new_full_name'] 
        new_date_of_birth = request.POST['new_dob'] or None
        new_date_of_death = request.POST['new_dod'] or None
        new_gender = request.POST['new_gender']
        new_fh_location = request.POST['new_fh_location']
        new_ssn = request.POST['new_ssn']

        if new_gender == 'male':
            new_gender_bool = True
        elif new_gender == 'female':
            new_gender_bool = False
        else:
            new_gender_bool = None

        location_cases = FH_Location.objects.filter(
            location = new_fh_location
        )
        if len(location_cases) == 0:
            case_id = 1

            new_case_id = FH_Location(
                case_id = case_id,
                location = new_fh_location
            )
            new_case_id.save()
        else:
            list_length = len(location_cases)
            list_length += 1
            case_id = list_length
            new_case_id = FH_Location(
                case_id = case_id,
                location = new_fh_location
            )
            new_case_id.save()

        new_case = Deceased_Info(
            name = new_full_name,
            date_of_birth = new_date_of_birth,
            date_of_death = new_date_of_death,
            case_id = new_case_id,
            ssn = new_ssn,
            male = new_gender_bool,
            staff_member = request.user
        )
        new_case.save()

        return HttpResponseRedirect(reverse('edit_case', args=[new_case.id]))
    

def edit_case(request, deceased_id):
    single_case_info = Deceased_Info.objects.get(id=deceased_id)
    single_event_info = Events.objects.filter(event_deceased_info=single_case_info)
    finance_info = Finances.objects.filter(finance_deceased_info=single_case_info)

    total_cost = 0
    for product in finance_info:
        total_cost += product.price
    total_cost = f"{total_cost:.2f}"
    
    
        

    if request.method == "POST":

        if single_case_info.completed:
            single_case_info.completed = False
        else:
            single_case_info.completed = True

        single_case_info.save()

        return HttpResponseRedirect(reverse('edit_case', args=[single_case_info.id]))
                    


    return render(request, 'myapp/edit_case.html', {
        "single_case_info": single_case_info,
        "single_event_info": get_eventlist(single_event_info),
        "finance_info": finance_info,
        "total_cost": total_cost
    })

    


@csrf_exempt    
def save_deceased_info(request, deceased_id):
    single_case_info = Deceased_Info.objects.get(id=deceased_id)
    # location_info = FH_Location.object.get(location=single_case_info)
    package = json.loads(request.body)
    print(single_case_info.case_id.location)
    
    personalInfoName = package['personalInfoName']
    single_case_info.name = personalInfoName

    personalInfoAddress = package['personalInfoAddress']
    single_case_info.address = personalInfoAddress

    personalInfoAge = package['personalInfoAge']
    if personalInfoAge == '':
        single_case_info.age = None
    else:
        single_case_info.age = int(personalInfoAge)

    personalInfoDOB = package['personalInfoDOB']
    if personalInfoDOB == '':
        single_case_info.date_of_birth = None
    else:
        single_case_info.date_of_birth = personalInfoDOB

    personalInfoDOD = package['personalInfoDOD']
    if personalInfoDOD == '':
        single_case_info.date_of_death = None
    else:
        single_case_info.date_of_death = personalInfoDOD
   

    personalInfoGender = package['personalInfoGender']

    if personalInfoGender == 'male':
        single_case_info.male = True
    elif personalInfoGender == 'female':
        single_case_info.male = False
    else:
        single_case_info.male = None

    # personalInfoLocation


    personalInfoSSN = package['personalInfoSSN']
    single_case_info.ssn = personalInfoSSN

    personalInfoNok = package['personalInfoNok']
    single_case_info.nok = personalInfoNok

    single_case_info.save()

    print(personalInfoGender)

    return JsonResponse({
        "message": "Case Updated!"
    })

@csrf_exempt    
def save_obituary(request, deceased_id):
    single_case_info = Deceased_Info.objects.get(id=deceased_id)
    package = json.loads(request.body)

    obituary = package['obituary']
    single_case_info.obituary = obituary
  


    single_case_info.save()

    return JsonResponse({
        "message": "Case Updated!"
    }) 


@csrf_exempt 
def save_finance(request, deceased_id):
    single_case_info = Deceased_Info.objects.get(id=deceased_id)
    package = json.loads(request.body)

    product = package['product']


    # dictionary will store product details
    product_services = {
        "Basic Service Fee": {
            'category':'Professional Services',
            'price':2195.00,
            'quantity': 1,
            'description': "Everything we do for you"
        },
        "Embalming": {
            'category':'Professional Services',
            'price':1095.00,
            'quantity': 1,
            'description': "Preservation and State requirement in certain circumstances"
        },
        "Embalming - Autopsy": {
            'category':'Professional Services',
            'price':1595.00,
            'quantity': 1,
            'description': "Preservation of autopsied remains and State requirement in certain circumstances"
        },
        "Private Goodbye": {
            'category':'Professional Services',
            'price':650.00,
            'quantity': 1,
            'description': "Private Setting to say goodbye, no embalming, 6 immediate family members, 15 minutes"
        },
        "Dressing, Casketing, and Cosmetizing": {
            'category':'Professional Services',
            'price':595.00,
            'quantity': 1,
            'description': "Dressing, Casketing, and Cosmetizing"
        },
        "Hair Dresser": {
            'category':'Professional Services',
            'price':90.00,
            'quantity': 1,
            'description': "Professional Hair Dressing"
        },
        "Visitation - Small": {
            'category':'Other Staff and Related Facilities',
            'price':1000.00,
            'quantity': 1,
            'description': "Small Viewing Room"
        },
        "Visitation - Medium": {
            'category':'Other Staff and Related Facilities',
            'price':1800.00,
            'quantity': 1,
            'description': "Medium Viewing Room"
        },
        "Visitation - Large": {
            'category':'Other Staff and Related Facilities',
            'price':2400.00,
            'quantity': 1,
            'description': "Large Viewing Room"
        },
        "Funeral Ceremony": {
            'category':'Other Staff and Related Facilities',
            'price':950.00,
            'quantity': 1,
            'description': "Day of Funeral"
        },
        "Memorial Service": {
            'category':'Other Staff and Related Facilities',
            'price':850.00,
            'quantity': 1,
            'description': "Day of Memorial"
        },
        "Graveside service": {
            'category':'Other Staff and Related Facilities',
            'price':250.00,
            'quantity': 1,
            'description': "License director to Final Disposition"
        },
        "Refrigeration": {
            'category':'Other Staff and Related Facilities',
            'price':175.00,
            'quantity': 1,
            'description': "Refrigeration, $175 per day"
        },
        "Transfer to Funeral Home": {
            'category':'Transportation',
            'price':595.00,
            'quantity': 1,
            'description': "Transfer to Funeral Home"
        },
        "Assistant on Transfer": {
            'category':'Transportation',
            'price':100.00,
            'quantity': 1,
            'description': "Assistant on Transfer"
        },
        "Hearse": {
            'category':'Transportation',
            'price':595.00,
            'quantity': 1,
            'description': "Hearse"
        },
        "Limousine": {
            'category':'Transportation',
            'price':495.00,
            'quantity': 1,
            'description': "Limousine"
        },
        "Flower Car": {
            'category':'Transportation',
            'price':375.00,
            'quantity': 1,
            'description': "Flower Car"
        },
        "Service Car": {
            'category':'Transportation',
            'price':375.00,
            'quantity': 1,
            'description': "Service Car"
        },
        "Casket": {
            'category':'Merchandise',
            'price':1.00,
            'quantity': 1,
            'description': "Casket"
        },
        "Vault or Outer Burial Container": {
            'category':'Merchandise',
            'price':1.00,
            'quantity': 1,
            'description': "Vault or Outer Burial Container"
        },
        "Urn": {
            'category':'Merchandise',
            'price':1.00,
            'quantity': 1,
            'description': "Urn"
        },
        "Prayer Cards per 100 Cards": {
            'category':'Merchandise',
            'price':200.00,
            'quantity': 1,
            'description': "Prayer Cards per 100 Cards"
        },
        "Register Book": {
            'category':'Merchandise',
            'price':45.00,
            'quantity': 1,
            'description': "Register Book"
        },
        "Acknowledgement cards (per box)": {
            'category':'Merchandise',
            'price':50.00,
            'quantity': 1,
            'description': "Acknowledgement cards (per box)"
        },
        "Crucifix or Cross": {
            'category':'Merchandise',
            'price':25.00,
            'quantity': 1,
            'description': "Crucifix or Cross"
        },
        "Flowers": {
            'category':'Merchandise',
            'price':1.00,
            'quantity': 1,
            'description': "Flowers"
        },
        "Cemetery": {
            'category':'Cash Disbursements',
            'price':1.00,
            'quantity': 1,
            'description': "Cemetery"
        },
        "Crematory": {
            'category':'Cash Disbursements',
            'price':1.00,
            'quantity': 1,
            'description': "Crematory"
        },
        "Church": {
            'category':'Merchandise',
            'price':1.00,
            'quantity': 1,
            'description': "Church"
        },
        "Clergy": {
            'category':'Cash Disbursements',
            'price':1.00,
            'quantity': 1,
            'description': "Clergy"
        },
        "Organist/Soloist": {
            'category':'Cash Disbursements',
            'price':1.00,
            'quantity': 1,
            'description': "Organist/Soloist"
        },
        "Certified Death Certificate": {
            'category':'Merchandise',
            'price':25.00,
            'quantity': 1,
            'description': "Certified Death Certificate"
        },
        "Additional Copies of Death Certificate": {
            'category':'Cash Disbursements',
            'price':2.00,
            'quantity': 1,
            'description': "Additional Copies of Death Certificate"
        },
        "Permit and Recording Fee": {
            'category':'Cash Disbursements',
            'price':20.00,
            'quantity': 1,
            'description': "Permit and Recording Fee"
        },
        "Newspaper": {
            'category':'Merchandise',
            'price':1.00,
            'quantity': 1,
            'description': "Newspaper"
        },
        "Gratuities": {
            'category':'Cash Disbursements',
            'price':1.00,
            'quantity': 1,
            'description': "Gratuities"
        },
        "Other": {
            'category':'Cash Disbursements',
            'price':1.00,
            'quantity': 1,
            'description': "Other"
        },

    }

#Keep populating



    
    new_product = Finances(
        finance_deceased_info = single_case_info, 
        name = product,
        category = product_services[product]['category'],
        description = product_services[product]['description'],
        quantity = product_services[product]['quantity'],
        price = product_services[product]['price'], 
    )
    new_product.save()

    return JsonResponse({
        "name": new_product.name,
        "category": new_product.category,
        "description": new_product.description,
        "quantity": new_product.quantity,
        "price": new_product.price,
        "id":new_product.id
     
    })





def add_event(request, deceased_id):
    single_case_info = Deceased_Info.objects.get(id=deceased_id)

    if request.method == "POST":
        # new_date_of_death = request.POST['new_dod']
        event_name = request.POST['new_event_name'] 
        event_location = request.POST['new_event_location'] 
        event_date = request.POST['new_event_date'] 
        event_time = request.POST['new_event_time'] 
        event_duration = request.POST['new_event_duration']


        new_event = Events(
            event_deceased_info = single_case_info,
            event_title = event_name,
            event_location = event_location,
            date = event_date,
            time = event_time,
            duration = event_duration
        )
        new_event.save()
        return HttpResponseRedirect(reverse('edit_case', args=[deceased_id]))
        

    else:
        return render(request, 'myapp/add_event.html', {
            "single_case_info": single_case_info,
        })
    
def edit_event(request, event_id):
    if request.method == "GET":
        print(event_id)
        single_event = Events.objects.get(id=event_id)
        print(single_event)
        return render(request, 'myapp/edit_event.html', {
            'single_event': single_event
        })
    else:
        event_name = request.POST['new_event_name'] 
        event_location = request.POST['new_event_location'] 
        event_date = request.POST['new_event_date'] 
        event_time = request.POST['new_event_time'] 
        event_duration = request.POST['new_event_duration']


        updated_event = Events.objects.get(id=event_id)
        
        updated_event.event_title = event_name
        updated_event.event_location = event_location
        updated_event.date = event_date
        updated_event.time = event_time
        updated_event.duration = event_duration
        
        updated_event.save()

        return HttpResponseRedirect(reverse('edit_case', args=[updated_event.event_deceased_info.id] ))
    
def delete_event(request, event_id):
    row_to_delete = Events.objects.get(id=event_id)
    deceased_id = row_to_delete.event_deceased_info.id
    row_to_delete.delete()
    return HttpResponseRedirect(reverse('edit_case', args=[deceased_id]))

@csrf_exempt
def edit_product(request, product_id):
    product = Finances.objects.get(id=product_id)
    package = json.loads(request.body)

    update_price = package['update_price']
    update_notes = package['update_notes']
    update_quantity = package['update_quantity']

    new_total = update_price * update_quantity

    product.price = new_total
    product.notes = update_notes
    product.quantity = update_quantity

    product.save()

    return JsonResponse({
        "message": "Product Updated!",
        "price": product.price,
        "notes": product.notes,
        "quantity": product.quantity
    })





def delete_product(request, product_id):
    product_to_delete = Finances.objects.get(id=product_id)

    print(product_to_delete.finance_deceased_info)

    product_to_delete.delete()
    deceased_id= product_to_delete.finance_deceased_info.id

    return HttpResponseRedirect(reverse('edit_case', args=[deceased_id]))







    
