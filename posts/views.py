from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Post
from .forms import PostForm


# Create your views here.

def post_home(request):
    return HttpResponse("<h1>Hello. This is the home page</h1>")

def post_list(request):
    querysetlist = Post.objects.filter(draft=False)
   
    paginator = Paginator(querysetlist, 4)

    page = request.GET.get('page')
    try:
       queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    #   query = request.GET.get("search")

    #if query:
    #    queryset = queryset.filter(
     #       Q(title__icontains = query) |
      #      Q(content__icontains = query)
       # ).distinct()

    context = {
        "object_list" : querysetlist,
        "title" : "Blog Posts",
    }
    return render(request, "post_list.html", context)

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        
        messages.success(request, "Successfully added this post")
        return HttpResponseRedirect(instance.get_absolute_url())
 
    context = {  
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    context = {
        "title": "Detail",
        "instance": instance,
    }
    return render(request, "post_detail.html", context)


def post_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        print form.cleaned_data.get("title")
        instance.save()
        messages.success(request, "Post is updated")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_delete(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    return redirect("posts:list")

    