"""
URL configuration for DiabetesPrediction project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth pages
    path('', views.login_view, name='login'),  # Login is root page
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # Core pages
    path('home/', views.home, name='home'),  # Home (after login)
    path('bmi/', views.bmi_calculator, name='bmi'),  # BMI Calculator Page
    path('predict/', views.predict, name='predict'),  # Prediction Form Page
    path('predict/result/', views.result, name='result'),  # Prediction Result Page
    path("chart/", views.chart_view, name="chart"),
    path('meal-plan/', views.meal_plan_view, name='meal_plan'),
    path('what-if-food/', views.what_if_food, name='what_if_food'),
    path('puzzle/', views.puzzle_view, name='puzzle'),
    path('update_score/', views.update_score, name='update_score'),





]
