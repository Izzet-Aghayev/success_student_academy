from django.urls import path

from . import views


app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name='courses'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('teachers/', views.teachers, name='teachers'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('registration/', views.registration, name='registration'),
    path('feedback/', views.feedback, name='feedback'),
]
