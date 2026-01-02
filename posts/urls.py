from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='home'),
    path('posts/', views.ArticleListView.as_view(), name='post_list'),
    path('popular/', views.PopularArticleListView.as_view(), name='popular_posts'),
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('bookmarks/', views.BookmarkListView.as_view(), name='bookmark_list'),
    path('category/<slug:slug>/', views.CategoryArticleListView.as_view(), name='category_posts'), 
    path('create/', views.ArticleCreateView.as_view(), name='post_create'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='post_detail'), 
    path('<int:pk>/update/', views.ArticleUpdateView.as_view(), name='post_update'), 
    path('<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='post_delete'), 
    path('<int:pk>/rate/<int:value>/', views.RatingToggleView.as_view(), name='post_rate'),
    path('<int:pk>/bookmark/', views.BookmarkToggleView.as_view(), name='post_bookmark'),
]