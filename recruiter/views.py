from django.shortcuts import render,redirect
from django.contrib.auth import login, logout,authenticate
from django.http import HttpResponse
from internfair.models import *
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
# Create your views here.
from internfair.models import *
from .models import *


def RecruiterLanding(request):
    if request.user.is_authenticated:
        if request.user.is_startup:
            return HttpResponseRedirect(reverse('recruiter:Profile',kwargs={'pk': request.user.id}))
        else:
            template = "recruiter/RecruiterLanding.html"
            return render(request,template)
    else:
        template = "recruiter/RecruiterLanding.html"
        return render(request,template)


# def RecruiterRegistration(request):
#     template = "recruiter/RecruiterRegistration.html"
#     return render(request, template)

@login_required(login_url='/recruiter')
def AvailableInterns(request,**kwargs):

    startup_object = StartUps.objects.get(user=request.user)
    template = "recruiter/AvailableInterns.html"

    Applications = InternApplication.objects.filter(Internship__startup = startup_object).filter(Status="PENDING")
    context = {'startup': startup_object, 'app': Applications}

    return render(request, template,context)


@login_required(login_url='/recruiter')
def ShortlistedInterns(request,**kwargs):
    if request.user.is_authenticated:
        startup_object = StartUps.objects.get(user=request.user)
        AllApplications = InternApplication.objects.filter(Internship__startup=startup_object)
        Applications = AllApplications.filter(Status='SHORTLISTED')
        template = "recruiter/ShortlistedInterns.html"
        if kwargs:

            pk = kwargs['pk']
            # print(pk)
            intern = AllApplications.get(id = pk)

            intern.Status = 'SHORTLISTED'
            intern.save()

        return render(request, template,{'startup': startup_object, 'app': Applications})
    else:
        return redirect('recruiter:RecruiterLanding')

@login_required(login_url='/recruiter')
def RejectedInterns(request,**kwargs):
    if request.user.is_authenticated:
        startup_object = StartUps.objects.get(user=request.user)
        AllApplications = InternApplication.objects.filter(Internship__startup=startup_object)
        Applications = AllApplications.filter(Status='REJECTED')
        template = "recruiter/RejectedInterns.html"
        if kwargs:

            pk = kwargs['pk']
            # print(pk)
            intern = AllApplications.get(id = pk)

            intern.Status = 'REJECTED'
            intern.save()

        return render(request, template,{'startup': startup_object, 'app': Applications})
    else:
        return redirect('recruiter:RecruiterLanding')


def app_status(request,**kwargs):
    dict=[]
    startup_object = StartUps.objects.all()
    for startup_temp in startup_object:
        AllApplications = InternApplication.objects.filter(Internship__startup=startup_temp)
        Rejected = AllApplications.filter(Status='REJECTED')
        Shortlisted = AllApplications.filter(Status='SHORTLISTED')
        Pending = AllApplications.filter(Status='PENDING')
        temp = {"Startup": startup_temp.companyName, "Rejected": Rejected.count(), "Shortlisted": Shortlisted.count(), "Pending": Pending.count(), "Total": AllApplications.count()}
        dict.append(temp)
    print(dict)
    template = "recruiter/app_status.html"
    return render(request, template,{'data': dict})

def add_profiles(request):
    template = "recruiter/AvailableInterns.html"
    return render(request, template)


@login_required
def CompanyProfile(request,**kwargs):
    current_user = request.user
    startup_object = StartUps.objects.get(user=current_user)
    profiles = Intern_form.objects.filter(startup_id = startup_object.id).filter(FormStatus = 'ACTIVE')
    template = "recruiter/CompanyProfile.html"
    return render(request, template,{'startup': startup_object,'profiles':profiles})

@login_required
def DeactivateForm(request,pk):

    id = pk
    current_user = request.user
    startup_object = StartUps.objects.get(user=current_user)
    form = Intern_form.objects.get(pk = id)
    # print(form)
    form.FormStatus = 'DEACTIVE'
    form.save()
    return HttpResponseRedirect(reverse('recruiter:Profile',kwargs={'pk': request.user.id}))

@login_required
def EditStartupProfile(request, **kwargs):
    current_user = request.user
    startup = StartUps.objects.get(user=current_user)
    if request.method=='POST':
      
        if len(request.FILES) != 0:
            startup.logo = request.FILES['startup_logo']
        if request.POST['companyName']:
            startup.companyName = request.POST['companyName']
        if request.POST['description']:
            startup.description = request.POST['description']
        if request.POST['location']:
            startup.location = request.POST['location']
        startup.save()
    return HttpResponseRedirect(reverse('recruiter:Profile',kwargs={'pk': current_user.id}))



@login_required
def intern_form(request):

    if request.method == "POST":
        # print(request.POST)
        startup = StartUps.objects.get(user=request.user)
        profile = request.POST["PROFILE"]
        stipend = request.POST["STIPEND"]
        allowances = request.POST["ALLOWANCE"]
        location = request.POST["LOCATION"]
        remarks = request.POST["REMARKS"]
        questions =  f'{request.POST["Q1"]}$${request.POST["Q2"]}$${request.POST["Q3"]}'

        form = Intern_form.objects.create(startup = startup,profile=profile,stipend=stipend,allowances=allowances,location=location,questions=questions, remarks=remarks)
        form.save()
        # print(form)
        return HttpResponseRedirect(reverse('recruiter:Profile',kwargs={'pk': request.user.id}))


@login_required
def logout_view(request):
    logout(request)
    return redirect('recruiter:RecruiterLanding')


