from django import forms
from internfair.models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator
# from django.contrib.auth.models import User
from django.db import transaction

class StartUpsForm(UserCreationForm):
    email = forms.EmailField(max_length=150, label='Email')
    POC = forms.CharField(max_length=50,label='Point Of Contact')
    contact = forms.IntegerField(label='Contact No.', validators=[MaxValueValidator(9999999999)])
    company_name = forms.CharField(max_length=100,label='Startup Name')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','email','POC','contact','company_name','password1', 'password2',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_startup = True
        user.save()
        startup = StartUps.objects.create(user=user)
        startup.email=self.cleaned_data.get('email')
        startup.POC=self.cleaned_data.get('POC')
        startup.companyName=self.cleaned_data.get('company_name')
        startup.contact=self.cleaned_data.get('contact')
        startup.save()
        return user

class StudentsForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    roll_number = forms.IntegerField(validators=[MaxValueValidator(999999999)])
    IITG_webmail = forms.EmailField(max_length=150,label='IITG Webmail')
    department = forms.CharField(max_length=50)
    contact= forms.IntegerField(validators=[MaxValueValidator(9999999999)],label='Contact No.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('name','username','IITG_webmail','roll_number','department','contact','password1', 'password2',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student =Students.objects.create(user=user)
        student.name=self.cleaned_data.get('name')
        student.roll_number=self.cleaned_data.get('roll_number')
        student.email=self.cleaned_data.get('IITG_webmail')
        student.department=self.cleaned_data.get('department')
        student.contact=self.cleaned_data.get('contact')
        student.save()
        return user

class ApplicationForm(forms.Form):
    resume = forms.FileField()
    content = forms.CharField(max_length=100)

class LogoForm(forms.Form):
    logo = forms.ImageField()

