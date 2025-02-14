from rest_framework import serializers
from warrior_point.models import Category, Game, SystemRequirement, Comment, Rating


# Класс сериализации объектов Модели Категории
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['cat_name']
#
#
# # Сериализатор для получения комментариев
# class CommentSerializer(serializers.ModelSerializer):
#     user = serializers.SlugRelatedField('username', read_only=True)
#
#     class Meta:
#         model = Comment
#         fields = ('text', 'user', 'created_at')
#
#
# # Сериализавтор для добавления комментариев
# class CommentCreateSerializer(serializers.Serializer):
#     text = serializers.CharField()
#     user_id = serializers.IntegerField()
#     game_id = serializers.IntegerField()
#
#     def create(self, validated_data):
#         return Comment.objects.create(**validated_data)
#
#
# class CommentCreateSerializer2(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ('text', 'user', 'game')
#
#
# class NewCategorySerializer(serializers.Serializer):
#     cat_name = serializers.CharField(max_length=255)
#
#     def create(self, validated_data):
#         print(validated_data, '====================')
#         return Category.objects.create(**validated_data)
#
#
# class SystemSerializer(serializers.Serializer):
#     op_system = serializers.CharField()
#     processor = serializers.CharField()
#     ram = serializers.CharField()
#     video_card = serializers.CharField()
#     memory = serializers.CharField()
#
#     def update(self, instance, validated_data):
#         instance.op_system = validated_data.get('op_system', instance.op_system)
#         instance.processor = validated_data.get('processor', instance.processor)
#         instance.ram = validated_data.get('ram', instance.ram)
#         instance.video_card = validated_data.get('video_card', instance.video_card)
#         instance.memory = validated_data.get('memory', instance.memory)
#         instance.save()
#         return instance
#
#
# class GameSerializer(serializers.Serializer):
#     title = serializers.CharField()
#     content = serializers.CharField()
#     image = serializers.ImageField()
#     created_at = serializers.DateTimeField()
#     category = serializers.SlugRelatedField(slug_field='cat_name', read_only=True)
#     requirements = SystemSerializer(many=True)
#     comments = CommentSerializer(many=True)
#
#
# # Сериализер для добавления игры
# class GameCreateSerializer(serializers.Serializer):
#     title = serializers.CharField()
#     content = serializers.CharField()
#     category_id = serializers.IntegerField()
#
#     def create(self, validated_data):
#         requirements = validated_data.pop('requirements', [])
#         game = Game.objects.create(**validated_data)
#         SystemRequirement.objects.create(game=game, **requirements[0])
#         return game
#
#     # Метод для изменения игры
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.content = validated_data.get('content', instance.content)
#         instance.category_id = validated_data.get('category_id', instance.category_id)
#         instance.save()
#         return instance


# Сериализаторы для вьюшек классов

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



class GamesSerializer(serializers.ModelSerializer):
    count_views = serializers.IntegerField()
    category = serializers.SlugRelatedField('cat_name', read_only=True)

    class Meta:
        model = Game
        exclude = ('video', 'torrent', 'views')



class RequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemRequirement
        exclude = ('game', )

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('game', 'updated_at')


class GameDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField('cat_name', read_only=True)
    requirements = RequirementsSerializer(many=True)
    comments = CommentsSerializer(many=True)
    count_views = serializers.IntegerField()
    star = serializers.FloatField()

    class Meta:
        model = Game
        fields = ('title', 'content', 'count_views', 'star', 'image', 'video',
                  'created_at', 'category', 'torrent', 'requirements', 'comments')


class CommentCreateSerializer(serializers.ModelSerializer):
    # Присваиваем автора комментария Автоматически
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('text', 'user', 'game')


class RatingAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('star', 'game')

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            game=validated_data.get('game', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating


