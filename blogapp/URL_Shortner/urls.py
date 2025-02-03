
from django.urls import path
from . import views

urlpatterns = [
   path("", views.home_page, name='home_page'),

    # URL click analytics for all URLs
    path('all_analytics/', views.all_analytics, name='all_analytics'),

    # Analytics for a specific short URL
    path('<slug:short_url>/', views.link_analytics, name='analytics'),

    # Redirect to long URL from short URL (not commented out)
    path('<slug:short_url>/redirect/', views.redirect_url, name='redirect_url'),  # Updated to use '/redirect/'
]



#  we need to render dynamic html/css/js file  
#  template helps to render dynamic page <==> change accordinf to database 
#  HttpResponse ==> response as a string 
# 