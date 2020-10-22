from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.books),
    path('books/add',views.addBook),
    path('books/create', views.createBook),
    path('books/<int:id>', views.oneBook),
    path('users/<int:id>', views.oneUser),
    path('books/delete/<int:id>', views.delete),
    path('review/create/<int:id>', views.createReview),
    path('logout', views.logout)
]



#First page - register and login - GET
    #POST - handle register
    #POST - handle login
#Second page - dashboard with users reviews - GET
#Third page - form for adding a book - GET
    #POST - add a book and review
#Fourth page - one book - GET
#Fifth page - one user - GET
#GET - delete a review