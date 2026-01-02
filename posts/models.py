from django.db import models
from django.conf import settings
from django.db.models import Sum, ExpressionWrapper, IntegerField, F
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Name')
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', verbose_name='Author')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Category')
    title = models.CharField(max_length=255, verbose_name='Title')
    content = models.TextField(verbose_name='Content')

    image = models.ImageField(upload_to='post_images/', blank=True, null=True, verbose_name='Image')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    is_draft = models.BooleanField(default=False, verbose_name='Is Draft')
    is_approved = models.BooleanField(default=False, verbose_name='Is Approved (Admin)')


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    @property
    def rating(self):
        """Calculates the average rating (1 to 5)."""
        votes = self.ratings.aggregate(
            total_votes=models.Count('id'),
            total_score=Sum(ExpressionWrapper(
                F('value') * 5 + (1 - F('value')) * 1,
                output_field=IntegerField()
            ))
        )
        
        if votes['total_votes'] and votes['total_votes'] > 0:
            return round(votes['total_score'] / votes['total_votes'], 2) 
        return 0.0


class ArticleRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='ratings')
    value = models.BooleanField(default=True) 

    class Meta:
        unique_together = ('user', 'article')
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'



class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'article')
        verbose_name = 'Bookmark'
        verbose_name_plural = 'Bookmarks'