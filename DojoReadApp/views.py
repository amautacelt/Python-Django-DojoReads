from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

from .models import User, Book, Review

# Create your views here.

#First page - register and login - GET
def index(request):
    return render(request, "index.html")

    
#POST - handle register
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        u = User.objects.create(alias=request.POST['alias'], name=request.POST['name'], email=request.POST['email'], password=hash1)
        request.session['userid'] = u.id
        return redirect("/books")


#POST - handle login
def login(request):
    user = User.objects.filter(email=request.POST['email'])
    errors = {}
    if not user:
        errors['email'] = "Invalid email or password"
    else:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect("/books")
        else:
            errors['password'] = "Invalid email or password"
    
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        return redirect("/books")


#Second page - dashboard with users reviews - GET
def books(request):
    if 'userid' not in request.session:
        return redirect("/")
    else:
        context = {
            "loggedin": User.objects.get(id=request.session['userid']),
            "topBooks": Book.objects.all().order_by("-created_at")[:3],
            "allBooks": Book.objects.all()
        }
        return render(request, "books.html", context)


#Third page - form for adding a book - GET
def addBook(request):
    if 'userid' not in request.session:
        return redirect("/")
    return render(request, "addBook.html")


#POST - add a book and review
def createBook(request):
    errors = Book.objects.basic_validator(request.POST)
    reviewErrors = Review.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        if len(reviewErrors) > 0:
            for key, value in reviewErrors.items():
                messages.error(request, value)
        return redirect("/books/add")
    if len(reviewErrors) > 0:
        for key, value in reviewErrors.items():
            messages.error(request, value)
        return redirect("/books/add")
    else:
        b = Book.objects.create(title=request.POST['title'], author=request.POST['author'])
        user = User.objects.get(id=request.session['userid'])
        Review.objects.create(content=request.POST['content'], rating=request.POST['rating'], reviewer=user, bookReviewed=b)
        return redirect(f"/books/{b.id}")


#Fourth page - one book - GET
def oneBook(request, id):
    if 'userid' not in request.session:
        return redirect("/")
    context = {
        "one" : Book.objects.get(id=id)
    }
    return render(request, "oneBook.html", context)


#Fifth page - one user - GET
def oneUser(request, id):
    if 'userid' not in request.session:
        return redirect("/")
    context = {
        "one" : User.objects.get(id=id)
    }
    return render(request, "oneUser.html", context)


#GET - delete a review
def delete(request, id):
    if 'userid' not in request.session:
        return redirect("/")
    rev = Review.objects.get(id=id)
    rev.delete()
    return redirect(f"/books/{rev.bookReviewed.id}")


def createReview(request, id):
    u = User.objects.get(id=request.session['userid'])
    b = Book.objects.get(id=id)
    errors = Review.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/books/{id}")
    else:
        Review.objects.create(content=request.POST['content'], rating=request.POST['rating'], reviewer=u, bookReviewed=b)
        return redirect(f"/books/{id}")


def logout(request):
    request.session.clear()
    return redirect("/")