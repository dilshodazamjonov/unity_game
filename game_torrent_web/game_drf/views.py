from django.shortcuts import render
from django.http import HttpResponse
from warrior_point.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from warrior_point.tests import get_user_ip
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, CreateAPIView
from rest_framework import permissions

# Create your views here.
# @api_view(['GET', 'POST'])
# def category_list(request):
#     if request.method == 'GET':
#         categories = Category.objects.all()
#         serializer = NewCategorySerializer(categories, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         print(request.data)
#         serializer = NewCategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# @api_view()
# def game_list_view(request):
#     games = Game.objects.all()
#     serializer = GameSerializer(games, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['POST'])
# def game_create_view(request):
#     if request.method == 'POST':
#         serializer = GameCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# @api_view(['GET', 'POST'])
# def game_detail(request, pk):
#     game = get_object_or_404(Game, pk=pk)
#     if request.method == 'GET':
#         serializer = GameSerializer(game)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         data = request.data
#         data['user'] = request.user.id
#         data['game'] = game.pk
#         serializer = CommentCreateSerializer2(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def game_update_delete(request, pk):
#     game = Game.objects.get(pk=pk)
#     systems = get_object_or_404(SystemRequirement, game=game)  # SystemRequirement.objects.get(game=game)
#     if request.method == 'GET':
#         serializer = GameSerializer(game)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         data = request.data
#         requirements = data.pop('requirements', [])
#
#         serializer = GameCreateSerializer(game, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         system_serializer = SystemSerializer(systems, data=requirements[0], context={'request': request})
#         system_serializer.is_valid(raise_exception=True)
#         system_serializer.save()
#
#         serial = GameSerializer(game)
#         return Response(serial.data)
#
#     elif request.method == 'DELETE':
#         if not game:
#             return Response({'error': 'Game not found for delete'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#         game.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# ======================================== Вьюшки на классе APIView =============================

# class CategoryListView(APIView):
#     def get(self, request):
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)
#
#
# class GameListListView(APIView):
#     def get(self, request):
#         games = Game.objects.all().annotate(
#             count_views=models.Count(models.F('views'))
#         )
#         serializer = GamesSerializer(games, many=True)
#         return Response(serializer.data)
#
# class GameDetailView(APIView):
#     def get(self, request, pk):
#         game = Game.objects.annotate(count_views=models.Count(models.F('views')),
#                                      star=models.Sum(models.F('ratings__star__value')) / models.Count(models.F('ratings'))
#                                      ).get(pk=pk)
#         serializer = GameDetailSerializer(game)
#         return Response(serializer.data)
#
#     def post(self, request, pk):
#         game = Game.objects.get(pk=pk)
#         # request.data["user"] = request.user.id
#         request.data["game"] = game.pk
#         serializer = CommentCreateSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#
#
#
# class GameByCategoryView(APIView):
#
#     def get(self, request, pk):
#         games = Game.objects.filter(category=pk).annotate(
#             count_views=models.Count(models.F('views'))
#         )
#         serializer = GamesSerializer(games, many=True)
#         return Response(serializer.data)
#
#
#
# class AddRatingView(APIView):
#     def post(self, request, pk):
#         game = get_object_or_404(Game, pk=pk)
#         request.data["game"] = game.pk
#         serializer = RatingAddSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(ip=get_user_ip(request))
#             return Response(status=status.HTTP_201_CREATED)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


# ===============================================  классы generics =======


class CategoryListApiView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GameListApiView(ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GamesSerializer

    def get_queryset(self):
        games = Game.objects.all().annotate(
            count_views=models.Count(models.F('views'))
        )
        return games

class GameDetailApiView(RetrieveAPIView):
    serializer_class = GameDetailSerializer

    def get_queryset(self):
        game = Game.objects.annotate(
            count_views=models.Count(models.F('views')),
            star=models.Sum(models.F('ratings__star__value')) / models.Count(models.F('ratings'))
        ).all()

        return game


class CommentCreateApiView(ListCreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        game = Game.objects.get(pk=self.kwargs['pk'])
        comments = Comment.objects.filter(game=game)
        return comments



class AddRatingApiView(CreateAPIView):
    serializer_class = RatingAddSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_user_ip(self.request))


class GameListByCategoryView(ListAPIView):
    serializer_class = GamesSerializer

    def get_queryset(self):
        games = Game.objects.filter(category=self.kwargs['pk']).annotate(
            count_views=models.Count(models.F('views'))
        )
        return games

