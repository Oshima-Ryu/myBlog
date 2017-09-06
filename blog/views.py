# import markdown.extensions.extra
# import markdown.extensions.codehilite
# import markdown.extensions.toc
import  markdown
from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse
from .models import Post, Category
from comments.forms import CommentForm
from comments.models import Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView,DetailView

def index(request):
    #return HttpResponse("hello world!")
    post_list = Post.objects.all().order_by('-create_time')
    paginator = Paginator(post_list,3)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context = {
        'post_list':post_list,
    }
    return render(request, 'blog/index.html', context=context)

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 3

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {'post':post,
               'form':form,
               'comment_list':comment_list
               }
    return render(request, 'blog/detail.html', context=context)

def archives(request, year, month):
    post_list = Post.objects.filter(create_time__year = year,
                                    create_time__month = month
                                    ).order_by('-create_time')
    context = {
        'post_list':post_list,
    }
    return render(request, 'blog/index.html', context=context)

class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        return super(ArchivesView, self).get_queryset().filter(create_time__year=self.kwargs.year).filter(create_time__month = self.kwargs.month)

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    print cate
    post_list = Post.objects.filter(category = cate).order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)