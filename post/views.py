from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, Http404
from .models import Post
from .forms import PostForm, CommentForm
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib import messages
from django.db.models import Q

# Create your views here.

def post_index(request):
    post_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(Q(title__icontains=query)|
                                     Q(content__icontains = query)|
                                     Q(user__first_name__contains=query)|
                                     Q(user__last_name__contains=query)).distinct()
    paginator = Paginator(post_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, "post/index.html", {'posts': posts})


def post_detail(request,
                slug):  # yorite detailleri id boyunca tapmagy ucin parametrda id-ni ulandyk ashaky bolumde hem id=id dp gorkezdik
    post = get_object_or_404(Post, slug=slug)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return HttpResponseRedirect(post.get_absolute_url())
    context = {
        "post": post,
        "form": form
    }
    return render(request, "post/detail.html", context)


@login_required
def post_create(request):
    # if request.method =="POST":
    #     print(request.POST)
    # title = request.POST.get('title')
    # content = request.POST.get('content')
    # Post.objects.create(title=title, content=content)
    # if request.method == "POST":
    #     #Formdan gelen bilgileri kaydet
    #     form = PostForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    # else:
    #     #Formu kullaniciya goster
    #     form = PostForm()

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, 'Başarili bir şekilde oluşturdunuz!')
        return HttpResponseRedirect(post.get_absolute_url())
    context = {
        'form': form,

    }
    return render(request, 'post/form.html', context)


@login_required
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, 'Başarili bir şekilde düzenlediniz!')
        return HttpResponseRedirect(post.get_absolute_url())
    context = {
        'form': form
    }

    return render(request, 'post/form.html', context)


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect("post:index")
