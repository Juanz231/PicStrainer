from django.urls import path
from . import views

urlpatterns = [
 #path('signupaccount/', views., name='signupaccount'),
 #path('logout/', views.logoutaccount, name='logoutaccount'),
 #path('login/', views.loginaccount, name='loginaccount'),
 path('Docs/', views.upload_doc, name='upload_doc'),
 path('visualizationDocs/', views.Show_Images, name='visulizationDocs'),
]