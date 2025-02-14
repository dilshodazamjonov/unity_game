from django.contrib.auth.models import User
from django.db import models


# Create your models here.
# Модель - таблицы бызы данных который имеет связь
from django.urls import reverse


class Category(models.Model):
    cat_name = models.CharField(max_length=255, verbose_name='Название категории')

    def __str__(self):
        return self.cat_name

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk':self.pk})


    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'



# Модель таблицы Бд игры
class Game(models.Model):
    title = models.CharField(max_length=300, verbose_name='Название игры')
    content = models.TextField(verbose_name='Опсиание')
    image = models.ImageField(upload_to='image/', blank=True, null=True, verbose_name='Картинка')  # blank=True, null=True делаем поле не обязательным для заполнения
    video = models.FileField(upload_to='video/', blank=True, null=True, verbose_name='Видео')
    views = models.ManyToManyField('Ip', related_name='game_views', blank=True, verbose_name='Просмотры')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    torrent = models.FileField(upload_to='torrents/', blank=True, null=True, verbose_name='Торрент файлы')

    def __str__(self):
        return self.title

    # метод для получения кол-ва просмотров
    def get_count_views(self):
        if self.views:
            return self.views.count()
        else:
            return 0

    def get_absolute_url(self):
        return reverse('game', kwargs={'pk':self.pk})

    def get_photo(self):  # Методдля получения картинки игры
        if self.image:
            return self.image.url
        else:
            return ''

    def get_video(self): # Методдля получения видео игры
        if self.video:
            return self.video.url
        else:
            return ''



    class Meta:
        verbose_name = 'Игру'
        verbose_name_plural = 'Игры'


# Модель таблицы БД Системные требования к игре
class SystemRequirement(models.Model):
    op_system = models.CharField(max_length=255, verbose_name='Операционная система')
    processor = models.CharField(max_length=255, verbose_name='Процессор')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    video_card = models.CharField(max_length=255, verbose_name='Видео карта')
    memory = models.CharField(max_length=255, verbose_name='Память')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Игра', related_name='requirements')

    def __str__(self):
        return self.game.title


    class Meta:
        verbose_name = 'Системные требования'
        verbose_name_plural = 'Системные требования'



class Comment(models.Model):
    text = models.CharField(max_length=500, verbose_name='Комментарий')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             default='user', verbose_name='Пользователь')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Игруля', related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')


    def __str__(self):
        return self.user.username


    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарий'




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватака', blank=True, null=True)
    about = models.CharField(max_length=150, verbose_name='О пользователе', blank=True, null=True)
    publisher = models.BooleanField(default=True, verbose_name='Право на публикации')
    city = models.CharField(max_length=100, default='Не указан', verbose_name='Город пользователя')


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def get_avatar(self):  # Метод для получения аватки
        if self.avatar:
            return self.avatar.url
        else:
            return 'https://nztcdn.com/avatar/l/1714939483/8368290.webp'



class Ip(models.Model):
    ip = models.CharField(max_length=150, verbose_name='Апи пользователя')

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = 'Ip пользователя'
        verbose_name_plural = 'Ip пользователей'


class RatingStar(models.Model):
    value = models.SmallIntegerField(default=0, verbose_name='Значение')

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Звезду рейтинга'
        verbose_name_plural = 'Звёзды рейтинга'


class Rating(models.Model):
    ip = models.CharField(max_length=50, verbose_name='IP Адрес пользователя')
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Звезда', default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='ratings', verbose_name='Игра')

    def __str__(self):
        return f'{self.game.title} - {self.star} : {self.ip}'

    class Meta:
        verbose_name = 'Рейтинг игры'
        verbose_name_plural = 'Рейтинги игр'








