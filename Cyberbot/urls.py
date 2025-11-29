from django.urls import path


from . import views

from .views import train_model




app_name = 'Cyberbot'

urlpatterns = [
    # Home
    path('', views.home, name='home'),


    # Simple page
    path('hello/', views.hello_world, name='hello_world'),

    # Cyber main pages
    path('cyber.html/', views.cyber, name='cyber'),

    path('cyber.html/login.html', views.login_view, name='login'),

    # New login pages (must exist in views.py)
    path('cyber/login/email/', views.email_view, name='email'),
    path('cyber/login/verify/', views.verify_view, name='verify'),

    # Reset password (must exist in views.py)
    path('reset-password/', views.reset_password_view, name='reset_password'),

    # Cyberbot section
    path('cyber.html/cyberbot.html', views.cyberbot, name='cyberbot'),
    path('cyber.html/chatbot.html', views.chatbot, name='chatbot'),

    # Image Fake/Real checker
      path('cyber/fakerealimage', views.my_view, name='fakerealimage'),

    # API section
    path('api/', views.api_index, name='api_index'),
    path('api/check-password-complete/', views.check_password_complete, name='check_password_complete'),
    path('api/check-url-safety/', views.check_url_safety, name='check_url_safety'),
     path("predict_api/", views.predict_api, name="predict_api"),


path('train/', train_model, name='train_model'),


]


