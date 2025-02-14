from django.urls import path
from .views import *

urlpatterns = [
    # path('api/v1/categories/', category_list),
    # path('api/v1/games/', game_list_view),
    # path('api/v1/game/<int:pk>/', game_detail),
    # path('api/v1/game_create/', game_create_view),
    # path('api/v1/game_update_del/<int:pk>/', game_update_delete)

    # ================== Пути для классов APIView ===================
    # path('api/v1/categories/', CategoryListView.as_view()),
    # path('api/v1/games/', GameListListView.as_view()),
    # path('api/v1/game/<int:pk>/', GameDetailView.as_view()),
    # path('api/v1/game/category/<int:pk>/', GameByCategoryView.as_view()),
    # path('api/v1/add_rating/<int:pk>/', AddRatingView.as_view())

    # ================== Пути для классов generics ===================
    path('api/v1/categories/', CategoryListApiView.as_view()),
    path('api/v1/games/', GameListApiView.as_view()),
    path('api/v1/game/<int:pk>/', GameDetailApiView.as_view()),
    path('api/v1/comments/<int:pk>/', CommentCreateApiView.as_view()),
    path('api/v1/add_rating/', AddRatingApiView.as_view()),
    path('api/v1/game/category/<int:pk>/', GameListByCategoryView.as_view()),
]



