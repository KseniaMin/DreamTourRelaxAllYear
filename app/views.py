"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import AnketaForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.db import models
from .models import Blog
from .forms import BlogForm

from .models import Comment # использование модели комментариев
from .forms import CommentForm # использование формы ввода комментария



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
            'about_us': 'О нас'
        }
    )

def links(request):
    resources = [
        {
            'url': 'https://vk.com/otdykh_kruglyi_god',
            'img_src': 'app/content/vk_logo.jpg',
            'alt_text': 'Официальная страница ВКонтакте'
        },
        {
            'url': 'https://2gis.ru/pskov/firm/12666903233198851',
            'img_src': 'app/content/2gis_maps_logo.png',
            'alt_text': 'Местоположение Тур.агенства "Отдых круглый год" '
        },
        {
            'url': 'https://zoon.ru/pskov/hotels/turisticheskoe_agentstvo_otdyh_kruglyj_god/',
            'img_src': 'app/content/site_logo.jpg',
            'alt_text': 'Сайт с полезной информацией про агенство'
        },
    ]
    return render(request, 'app/links.html', {'resources': resources})

def anketa(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            # Если форма валидна, обработка данных отзыва
            return render(request, 'app/success.html', {'form': form})
    else:
        form = AnketaForm() 
    return render(request, 'app/anketa.html', {'form': form})

def success_view(request):
    """Render a success page."""
    return render(request, 'app/success.html')

def registration(request):
    """Renders the registration page."""

    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        regform = UserCreationForm(request.POST)

        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now()
            reg_f.save()
            return redirect('home')
    else:
        regform = UserCreationForm()

    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,
            'year': datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all()  # запрос на выбор всех статей блога из модели
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Блог',
            'posts': posts,  # передача списка статей в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)  # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)
    if request.method == "POST":  # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user  # добавляем автора комментария
            comment_f.date = datetime.now()  # добавляем текущую дату
            comment_f.post = Blog.objects.get(id=parametr)  # добавляем статью, для которой данный комментарий
            comment_f.save()  # сохраняем комментарий
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm()  # создание формы для ввода комментария
    return render(request, 'app/blogpost.html', {
        'post_1': post_1,  # передача конкретной статьи в шаблон веб-страницы
        'comments': comments,  # передача комментариев в шаблон веб-страницы
        'form': form,  # передача формы в шаблон веб-страницы
        'year': datetime.now().year,
    }
    )

def newpost(request): 
    """Renders the new post page."""
    assert isinstance(request, HttpRequest)
    blogform = BlogForm()   # инициализация переменной blogform

    if request.method == "POST":    # после отправки формы
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()           # сохраняем изменения после добавления полей
            return redirect('blog') # переадресация на страницу Блог после создания статьи Блога
            
    return render(
        request,
        'app/newpost.html',
        { 
            'blogform': blogform, # передача формы в шаблон веб-страницы
            'title': 'Добавить статью блога',
            'year':datetime.now().year,
        }
    )

def videopost(request):
    """Renders the video post page."""
    assert isinstance(request, HttpRequest)
    # Добавьте код здесь для обработки запроса и рендеринга страницы videopost
    return render(
        request,
        'app/videopost.html',
        {
            'title': 'Видеостатья',
            'message': 'Это видеостатья.',
            'year': datetime.now().year,
        }
    )


