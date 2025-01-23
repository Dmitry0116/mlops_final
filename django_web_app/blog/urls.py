from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    search,
    about
)

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),  # Главная страница блога
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),  # Посты пользователя
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # Детали поста
    path('post/new/', PostCreateView.as_view(), name='post-create'),  # Создание нового поста
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),  # Обновление поста
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # Удаление поста
    path('search/', search, name='search'),  # Поиск постов
    path('about/', about, name='blog-about'),  # О блоге
]
