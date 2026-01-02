from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.db.models import Q 
from .models import Article, Category, ArticleRating, Bookmark
from .forms import ArticleForm
from .mixins import AuthorOrAdminRequiredMixin


class BasePostListView(ListView):
    model = Article
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return Article.objects.filter(is_approved=True, is_draft=False).select_related('author', 'category')


class ArticleListView(BasePostListView):
    pass


class PopularArticleListView(BasePostListView):
    
    def get_queryset(self):
        articles = list(super().get_queryset())
        popular_articles = [a for a in articles if a.rating >= 4.0]
        return popular_articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginate_by)
        page = self.request.GET.get('page')
        context['posts'] = paginator.get_page(page)
        return context


class CategoryArticleListView(BasePostListView):
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug)
        return super().get_queryset().filter(category=category)


class AuthorListView(ListView):
    model = get_user_model()
    template_name = 'posts/author_list.html'
    context_object_name = 'authors'
    
    def get_queryset(self):
        return get_user_model().objects.filter(posts__is_approved=True).distinct()


class BookmarkListView(LoginRequiredMixin, BasePostListView):
    def get_queryset(self):
        return Article.objects.filter(bookmark__user=self.request.user).select_related('author', 'category')


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_admin_or_superadmin or user.is_superuser:
                return Article.objects.all().select_related('author', 'category')
            
            return Article.objects.filter(
                Q(is_approved=True) | Q(author=user)
            ).select_related('author', 'category')
        
        return Article.objects.filter(is_approved=True).select_related('author', 'category')

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'posts/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user

        if not form.cleaned_data.get('is_draft'):
             form.instance.is_approved = False 
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})



class ArticleUpdateView(AuthorOrAdminRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'posts/post_form.html'
    
    def form_valid(self, form):
       
        if not form.cleaned_data.get('is_draft') and not self.request.user.is_admin_or_superadmin:
            form.instance.is_approved = False 
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


class ArticleDeleteView(AuthorOrAdminRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('home')
    template_name = 'posts/post_confirm_delete.html'



class RatingToggleView(LoginRequiredMixin, View):
    def post(self, request, pk, value): 
        article = get_object_or_404(Article, pk=pk)
        
        ArticleRating.objects.update_or_create(
            user=request.user, 
            article=article, 
            defaults={'value': bool(int(value))}
        )
        
        return JsonResponse({'rating': article.rating})



class BookmarkToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, article=article)
        
        if not created:
            bookmark.delete()
            return JsonResponse({'bookmarked': False, 'message': 'Bookmark removed'})
        
        return JsonResponse({'bookmarked': True, 'message': 'Bookmark added'})