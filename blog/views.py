from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods,require_POST,require_GET
from .models import BlogCategory,BlogPost,BlogComment
from .forms import PubBlogForm
from django.db.models import Q
# Create your views here.
def index(request):
    blogs=BlogPost.objects.all()
    return render(request, 'index.html',context={'blogs':blogs})

def blog_detail(request, blog_id):
    try:
        blog = BlogPost.objects.get(pk=blog_id)
    except Exception as e:
        blog = None
    return render(request, 'blog_detail.html',context={'blog':blog})

@require_http_methods(['GET', 'POST'])
@login_required(login_url=reverse_lazy("zlauth:login"))
def pub_blog(request):
    if request.method == "GET":
        categories = BlogCategory.objects.all()
        return render(request, 'public.html',context={'categories':categories})
    else:
        form = PubBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            blog=BlogPost.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            return JsonResponse({"code":200, "msg":"发布成功","data":{"blog_id": blog.id}})
        else:
            print(form.errors)
            return JsonResponse({"code":400, "msg":"发布失败"})

@require_POST
@login_required
def pub_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComment.objects.create(content=content,blog_id=blog_id,author=request.user)
    return redirect(reverse('blog:blog_detail',kwargs={'blog_id': blog_id}))

@require_GET
def search(request):
    q=request.GET.get('q')
    blogs=BlogPost.objects.filter(Q(title__icontains=q)|Q(content__icontains=q)).all()
    return render(request, 'index.html',context={'blogs':blogs})

