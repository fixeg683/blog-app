from django.urls import path
from . import views

urlpatterns = [
    # The name='home' here is what {% url 'home' %} looks for
    path('', views.home, name='home'),
    
    # Other patterns required by your templates
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('add_blog/', views.add_blog, name='add_blog'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search, name='search'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog_update/<slug:slug>/', views.edit_blog_post, name='edit_blog_post'),
    path('blog_delete/<slug:slug>/', views.delete_blog_post, name='delete_blog_post'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]