from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model


class AuthorOrAdminRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()
        
        if not request.user.is_authenticated or request.user.is_banned:
             return self.handle_no_permission()

        if article.author == request.user or request.user.is_admin_or_superadmin:
            return super().dispatch(request, *args, **kwargs)
            
        return redirect(article.get_absolute_url())