from django.urls import include, path,re_path
from . import views
from internfair import views as stViews
from django.conf.urls.static import static
from django.conf import settings

app_name = 'recruiter'

urlpatterns = [

    path('', views.RecruiterLanding, name='RecruiterLanding'),
    path('registration', stViews.StartUpsRegistration.as_view(), name='RecruiterRegistration'),
    path('14_10_2000', views.app_status, name='app_status'),
    path(r'^interns/(?P<pk>\d+)/$', views.AvailableInterns, name='InternList'),
    path('shortlist/', views.ShortlistedInterns, name='shortlistedInterns'),
    path('rejected/', views.RejectedInterns, name='rejectedInterns'),
    path('shortlist/<int:pk>/', views.ShortlistedInterns, name='shortlistedInterns'),
    path('rejected/<int:pk>/', views.RejectedInterns, name='rejectedInterns'),
    path(r'^profile/(?P<pk>\d+)/$', views.CompanyProfile, name='Profile'),
    path(r'^profile/edit/(?P<pk>\d+)/$', views.EditStartupProfile, name='editStartupProfile'),
    path('profile/deactivate/<int:pk>', views.DeactivateForm, name='deactivate'),
    path('form', views.intern_form, name='form_submit'),
    path('login',stViews.startupLogin, name='StartupLogin'),
    path('logout',views.logout_view, name='StartupLogout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
