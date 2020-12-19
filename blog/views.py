from django.views.generic import ListView, DetailView
from .models import Blog, Category


class BlogPosts(ListView):
    model = Blog
    template_name = 'blog/blog.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BlogPosts, self).get_context_data(**kwargs)
        context['title'] = 'Блог'
        return context

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


class CategoryPosts(ListView):
    model = Blog
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryPosts, self).get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return Blog.objects.filter(category_id=self.kwargs['category_id'], is_published=True)


class ViewPost(DetailView):
    model = Blog
    pk_url_kwarg = 'post_id'
    template_name = 'blog/view_post.html'
    context_object_name = 'item'