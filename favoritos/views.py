from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from .decorators import loginauth

@loginauth
def index(request):
    context = {
        'books': Book.objects.all(),
        'user': User.objects.get(id=request.session['user'])
    }
    return render(request, 'favoritos.html', context)

def newbook(request):
    if request.method == 'POST':
        errors = Book.objects.validator(request.POST)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect("/librosfavoritos")
        newbook= Book.objects.create(
            title=request.POST['title'],
            description=request.POST['desc'],
            uploaded_by= User.objects.get(id=request.session['user']),
        )
        user = User.objects.get(id=request.session['user'])
        user.liked_books.add(newbook)
    return redirect('/librosfavoritos')

def like(request, id):
    book=Book.objects.get(id=id)
    user=User.objects.get(id=request.session['user'])
    user.liked_books.add(book)
    return redirect('/librosfavoritos')

def book(request, id):
    context = {
        'book': Book.objects.get(id=id),
        'user': User.objects.get(id=request.session['user'])
    }
    return render(request, 'book.html', context)

def update(request, id):
    book = Book.objects.get(id=id)
    book.title = request.POST['title']
    book.description = request.POST['desc']
    book.save()
    return redirect(f'/librosfavoritos/{id}')

@loginauth
def delete(request, id):
    book= Book.objects.get(id=id)
    book.delete()
    return redirect('/librosfavoritos')

@loginauth
def dislike(request, id):
    book = Book.objects.get(id=id)
    user = User.objects.get(id=request.session['user'])
    if book in user.liked_books.all():
        book.liked_by.remove(user)
        return redirect('/librosfavoritos')
    return redirect(f'/librosfavoritos/{id}')