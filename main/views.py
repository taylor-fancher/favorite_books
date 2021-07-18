from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def create_user(request):
    errors = User.objects.user_validator(request.POST)

    user = User.objects.filter(email=request.POST['email'])
    if user:
        messages.error(request, "Email already exists.")
        return redirect('/')

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
        
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    user1 = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed_pw,
    )
    request.session['log_user_id'] = user1.id
    return redirect('/dashboard')

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['log_user_id'] = logged_user.id
            return redirect('/dashboard')
    else:
            messages.error(request, 'Invalid email or password')
    messages.error(request, "Email does not exist")
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    context = {
        'user': User.objects.get(id=request.session['log_user_id']),
        'books': Book.objects.all()
    }
    return render(request, 'dashboard.html', context)

def create_book(request):
    errors = Book.objects.book_validator(request.POST)

    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/dashboard')
    
    book = Book.objects.create(
        title = request.POST['title'],
        desc = request.POST['desc'],
        uploaded_by = User.objects.get(id=request.session['log_user_id']),
    )
    book.liked_by.add(request.POST['user'])
    
    return redirect('/dashboard')

def one_book(request, id):
    context = {
        'this_book': Book.objects.get(id=id),
        'user': User.objects.get(id=request.session['log_user_id']),
    }
    return render(request, 'one_book.html', context)

def edit_book(request, id):
    context = {
        'book': Book.objects.get(id=id),
        'user': User.objects.get(id=request.session['log_user_id']),
    }

    book = Book.objects.get(id=id)

    if request.session['log_user_id'] != book.uploaded_by.id:
        return render(request, 'sorry.html', context)



    # errors = Book.objects.book_validator(request.POST)

    # if len(errors) > 0:
    #     for k, v in errors.items():
    #         messages.error(request, v)
    #     return redirect(f'/books/{book.id}/edit')

    return render(request, 'edit_book.html', context)

def edit(request, id):
    errors = Book.objects.book_validator(request.POST)

    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/dashboard')
    
    this_book = Book.objects.get(id=id)
    this_book.title = request.POST['title']
    this_book.desc = request.POST['desc']
    this_book.save()
    return redirect(f'/books/{this_book.id}')

def favorite(request, id):
    this_user = User.objects.get(id=request.session['log_user_id'])
    this_book = Book.objects.get(id=id)
    this_user.liked_books.add(this_book)
    return redirect(f'/book/{this_book.id}')

def delete(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect('/dashboard')

def your_favorites(request):
    context = {
        'user': User.objects.get(id=request.session['log_user_id'])
    }
    return render(request, 'your_favorites.html', context)

def unfavorite(request, id):
    this_user = User.objects.get(id=request.session['log_user_id'])
    this_book = Book.objects.get(id=id)
    this_user.liked_books.remove(this_book)
    return redirect('/your_favorites')

# Create your views here.
