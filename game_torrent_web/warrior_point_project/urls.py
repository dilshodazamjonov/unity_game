from django.urls import path
from .views import *

urlpatterns = [
    # path('', index, name='index'),
    # path('category/<int:pk>/', game_category_view, name='category'),
    # path('game/<int:pk>/', game_detail_view, name='game'),
    # path('new_game/', add_game_view, name='add_game'),

    path('', GameListView.as_view(), name='index'),
    path('category/<int:pk>/', GameByCategory.as_view(), name='category'),
    path('game/<int:pk>/', GameDetailView.as_view(), name='game'),
    path('login/', user_login_view, name='login'),
    path('logout/', user_logout_view, name='logout'),
    path('registration/', register_view, name='register'),
    path('new_game/', NewGame.as_view(), name='add_game'),
    path('game/<int:pk>/update/', GameUpdateView.as_view(), name='update'),
    path('game/<int:pk>/delete/', GameDeleteView.as_view(), name='delete'),
    path('search/', SearchGames.as_view(), name='search'),
    path('save_comment/<int:pk>/', save_comment_view, name='save_comment'),
    path('comment/<int:pk>/update/', CommentUpdate.as_view(), name='comment_update'),
    path('comment/<int:comment_pk>/<int:game_pk>/delete/', comment_delete, name='comment_delete'),
    path('download/<int:pk>/', download_torrent, name='download'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('change/<str:username>/', edit_account_profile_view, name='change'),
    path('edit_account/', edit_account_view, name='edit_account'),
    path('edit_profile/', edit_profile_view, name='edit_profile')
]
