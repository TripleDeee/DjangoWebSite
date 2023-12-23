from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like
from .forms import CommentForm
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import EmailUserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def logout_view(request):
    logout(request)
    return redirect('post_list')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('post_list')
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
    return render(request, 'registration/login.html')


def post_list(request):
    posts_list = Post.objects.all().order_by('-created_at')

    # Добавим пагинацию, чтобы отображать по 3 поста на каждой странице
    paginator = Paginator(posts_list, 3)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если параметр страницы не является целым числом, отображаем первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница вне диапазона (например, 9999), отображаем последнюю страницу
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_list.html', {'posts': posts})


@login_required(login_url='/login/')
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    likes_count = post.like_set.filter(is_like=True).count()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post_id)
    else:
        form = CommentForm()

    comments = post.comment_set.all().order_by('-created_at')

    return render(request, 'blog/add_comment.html', {'form': form, 'post': post, 'likes_count': likes_count, 'comments': comments})


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    likes_count = post.like_set.filter(is_like=True).count()

    comments = post.comment_set.all().order_by('-created_at')

    return render(request, 'blog/post_detail.html', {'post': post, 'likes_count': likes_count, 'comments': comments})

@login_required(login_url='/login/')
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    liked = Like.objects.filter(post=post, user=request.user, is_like=True).exists()

    if liked:
        Like.objects.filter(post=post, user=request.user, is_like=True).delete()
    else:
        Like.objects.filter(post=post, user=request.user, is_like=False).delete()
        Like.objects.create(post=post, user=request.user, is_like=True)

    post_detail_url = reverse('post_detail', kwargs={'pk': post_id})
    return redirect(post_detail_url)

def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = EmailUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
