from django.urls import path # import path, similar to project's urls.py
from . import views # import views.py from the currentdirectory

urlpatterns = [ path('', views.index, name='index'), ]
