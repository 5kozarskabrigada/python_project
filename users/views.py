from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.views import View
from django.urls import reverse_lazy
from django.http import JsonResponse
from .forms import CustomUserCreationForm, UserEditForm
from posts.models import Article, ArticleRating, Bookmark 


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})


class RatingToggleView(LoginRequiredMixin, View):
    def post(self, request, pk, value):
        article = get_object_or_404(Article, pk=pk)
        val_bool = bool(int(value)) 
        
        ArticleRating.objects.update_or_create(
            user=request.user, 
            article=article, 
            defaults={'value': val_bool}
        )
        return JsonResponse({'rating': article.rating})

class BookmarkToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, article=article)
        
        if not created:
            bookmark.delete()
            return JsonResponse({'bookmarked': False})
        
        return JsonResponse({'bookmarked': True})