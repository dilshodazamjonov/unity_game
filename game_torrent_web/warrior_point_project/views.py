from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from .models import Category, Game, SystemRequirement, Comment, Profile, Ip
from .forms import LoginForm, RegisterForm, GameForm, SystemForm, CommentForm, EditProfileForm, EditAccountFrom
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .tests import get_user_ip


# Create your views here.
# def index(request):
#     games = Game.objects.all()[::-1]
#     context = {
#         'games': games,
#         'title': 'Качай топ игры'
#     }
#
#     return render(request, 'warrior_point/index.html', context)

class GameListView(ListView):
    model = Game
    context_object_name = 'games'
    template_name = 'warrior_point/index.html'
    extra_context = {
        'title': 'Качай топ игры'
    }

# =========================================================================================================

# Вьюшка для получения игр по категории
# def game_category_view(request, pk):
#     games = Game.objects.filter(category_id=pk)[::-1]  # Получим игры по id категории
#     category = Category.objects.get(pk=pk)
#
#     context = {
#         'games': games,
#         'title': f'Качай {category.cat_name}'
#     }
#     return render(request, 'warrior_point/index.html', context)

class GameByCategory(GameListView):

    # Метод что бы переназначить вывод данных
    def get_queryset(self):
        games = Game.objects.filter(category_id=self.kwargs['pk'])
        return games

    # Метод при помощи которго допонительно можно отправить на страницу
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Качай {category.cat_name}'
        print(context)
        return context




# =========================================================================================================

# Вьюшка для страницы детали Игры
# def game_detail_view(request, pk):
#     game = Game.objects.get(pk=pk)  # Получим игру по id
#     systems = SystemRequirement.objects.get(game_id=pk)
#
#     context = {
#         'game': game,
#         'title': game.title,
#         'systems': systems
#     }
#     return render(request, 'warrior_point/game_detail.html', context)

class GameDetailView(DetailView):
    model = Game
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        game = Game.objects.get(pk=self.kwargs['pk'])  # Получим игру по id
        systems = SystemRequirement.objects.get(game_id=game.pk)
        context['systems'] = systems  # Отправляем системные требования
        context['title'] = game.title
        context['comments'] = Comment.objects.filter(game=game)

        ip = get_user_ip(self.request)
        if Ip.objects.filter(ip=ip).exists():
            game.views.add(Ip.objects.get(ip=ip))
        else:
            Ip.objects.create(ip=ip)
            game.views.add(Ip.objects.get(ip=ip))

        if self.request.user.is_authenticated:
            context['form'] = CommentForm()
        return context




# =========================================================================================================

# Вьюшка для Авторизации пользователя
def user_login_view(request):
    if request.method == 'POST':
        # Логика Авторизации
        form = LoginForm(data=request.POST) # Получим данные из формы
        if form.is_valid():  # Проверяем форму на валидность
            user = form.get_user()  # Метод для получения пользователя в бд по логину и паролю
            if user:
                login(request, user)
                messages.success(request, f'Добро пожаловать {user.username}')
                return redirect('index')
            else:
                messages.error(request, 'Ты олень ввёл не верный логин или пароль')
                return redirect('login')
        else:
            messages.error(request, 'Ты олень ввёл не верный логин или пароль')
            return redirect('login')

    else:
        form = LoginForm()

    context = {
        'title': 'Вход в Аккаунт',
        'login_form': form
    }
    if not request.user.is_authenticated:
        return render(request, 'warrior_point/login.html', context)
    else:
        return redirect('index')



# Вьюшка для выхода
def user_logout_view(request):
    logout(request)
    messages.warning(request, 'Уже уходите 😥')
    return redirect('index')


# Вьюшка для Регистрации
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            messages.success(request, 'Регистрация рошла успешно.\nАвторизуйтесь')
            return redirect('login')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('register')
    else:
        form = RegisterForm()

    context = {
        'title': 'Регистрация',
        'form': form
    }
    if not request.user.is_authenticated:
        return render(request, 'warrior_point/register.html', context)
    else:
        return redirect('index')

# =============================================================

# Вьюшка для добавления новой Игры
# def add_game_view(request):
#     if request.method == 'POST':
#         form = GameForm(request.POST, request.FILES)
#         system_form = SystemForm(request.POST)
#         if form.is_valid() and system_form.is_valid():
#             game = form.save()
#             game.save()
#             system = system_form.save(commit=False)
#             system.game = game
#             system.save()
#             return redirect('game', game.pk)
#         else:
#             return redirect('add_game')
#
#     else:
#         form = GameForm()
#         system_form = SystemForm()
#
#     context = {
#         'title': 'Добавить игру',
#         'form': form,
#         'system_form': system_form
#     }
#
#     return render(request, 'warrior_point/add_game.html', context)


class NewGame(CreateView):
    form_class = GameForm
    template_name = 'warrior_point/add_game.html'
    extra_context = {
        'title': 'Добавить игру'
    }
    # Метод проверки пользователя является ли он сотрудником
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect('index')
        else:
            return super(NewGame, self).get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['system_form'] = SystemForm()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        system_form = SystemForm(self.request.POST)
        if system_form.is_valid():
            system = system_form.save(commit=False)
            system.game = self.object
            system.save()
        return response

    # def post(self, request, *args, **kwargs):
    #     if request.method == 'POST':
    #         form = GameForm(request.POST, request.FILES)
    #         system_form = SystemForm(request.POST)
    #         if form.is_valid() and system_form.is_valid():
    #             game = form.save()
    #             game.save()
    #             system = system_form.save(commit=False)
    #             system.game = game
    #             system.save()
    #             return redirect('game', game.pk)
    #         else:
    #             return redirect('add_game')



class GameUpdateView(UpdateView):
    model = Game
    form_class = GameForm
    template_name = 'warrior_point/add_game.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect('index')
        else:
            return super(GameUpdateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        game = Game.objects.get(pk=self.kwargs['pk'])
        systems = SystemRequirement.objects.get(game=game)
        context['system_form'] = SystemForm(instance=systems)
        context['title'] = f'Изменить: {game.title}'
        return context


    def form_valid(self, form):
        response = super().form_valid(form)  # Полученную форму проверяем на валидность

        game = Game.objects.get(pk=self.kwargs['pk'])
        systems = SystemRequirement.objects.get(game=game)
        system_form = SystemForm(self.request.POST, instance=systems)
        if system_form.is_valid():
            system = system_form.save(commit=False)
            system.game = self.object
            system.save()
        return response



class GameDeleteView(DeleteView):
    model = Game
    context_object_name = 'game'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect('index')
        else:
            return super(GameDeleteView, self).get(request, *args, **kwargs)



# Вьющка для поиска игр
class SearchGames(GameListView):
    def get_queryset(self):
        word = self.request.GET.get('q')
        games = Game.objects.filter(title__iregex=word)
        return games



# Вьюшка для сохранения комментария
def save_comment_view(request, pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.game = Game.objects.get(pk=pk)
        comment.save()
        return redirect('game', pk)


class CommentUpdate(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'warrior_point/game_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        comment = Comment.objects.get(pk=self.kwargs['pk'])  # Получим коммент по id

        game = Game.objects.get(pk=comment.game.pk)  # Получим игру по id которую возьмём у коммента
        systems = SystemRequirement.objects.get(game_id=game.pk)
        comments = Comment.objects.filter(game=game)
        comments = [i for i in comments if i.pk != comment.pk]  # Получим все все комменты кроме того что изменяем
        context['game'] = game
        context['systems'] = systems  # Отправляем системные требования
        context['title'] = game.title
        context['comments'] = comments

        return context

    def get_success_url(self):
        return reverse('game', kwargs={'pk': self.object.game_id})



# Реализовать вьюшку для удаления коммента
def comment_delete(request, comment_pk, game_pk):
    user = request.user if request.user.is_authenticated else None
    if user:
        comment = Comment.objects.get(user=user, pk=comment_pk, game=game_pk)
        comment.delete()
    return redirect('game', game_pk)


# Вьюшка для скачки файла торрента
def download_torrent(request, pk):
    if request.user.is_authenticated:
        game = Game.objects.get(pk=pk)
        response = FileResponse(open(game.torrent.path, mode='rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename=%s' % game.torrent.name
        return response



def profile_view(request, username):
    user = request.user if request.user.is_authenticated else None
    if user:
        profile = Profile.objects.get(user=user)
        comments = Comment.objects.filter(user=user)
        count_comment = len(comments)

        context = {
            'title': f'Профиль: {user}',
            'profile': profile,
            'count': count_comment
        }

        return render(request, 'warrior_point/profile.html', context)

    else:
        messages.success(request, 'Авторизуйтесь что бы перйти в профиль')
        return redirect('login')


# Вьшка для страницы изменения Акаунта и профиля
def edit_account_profile_view(request, username):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        profile = Profile.objects.get(user=request.user)
        if profile:
            context = {
                'profile_form': EditProfileForm(instance=request.user.profile),
                'account_form': EditAccountFrom(instance=request.user),
                'title': f'Изменение данных {request.user.username}'
            }

            return render(request, 'warrior_point/edit.html', context)
        else:
            return redirect('login')




# Вьюшка для изменения аккаунта
def edit_account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            edict_account_form = EditAccountFrom(request.POST, instance=request.user)
            if edict_account_form.is_valid():
                edict_account_form.save()
                data = edict_account_form.cleaned_data  # Получим данные из формы в виде словоря
                user = User.objects.get(id=request.user.id)
                if user.check_password(data['old_password']):
                    if data['old_password'] and data['new_password'] == data['confirm_password']:
                        user.set_password(data['new_password'])
                        user.save()
                        update_session_auth_hash(request, user)  # Функция которая оставит нас авторизованными
                        messages.success(request, 'Данные успешно изменены')
                        return redirect('profile', user.username)
                    else:
                        for field in edict_account_form.errors:
                            messages.error(request, edict_account_form.errors[field].as_text())
                            return redirect('change', user.username)
                else:
                    for field in edict_account_form.errors:
                        messages.error(request, edict_account_form.errors[field].as_text())
                        return redirect('change', user.username)

                return redirect('profile', user.username)
            else:
                for field in edict_account_form.errors:
                    messages.error(request, edict_account_form.errors[field].as_text())
                    return redirect('change', request.user.username)




# Вьюшка для изменения профиля
def  edit_profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if form.is_valid():
                form.save()
                return redirect('profile', request.user.username)
            else:
                for field in form.errors:
                    messages.error(request, form.errors[field].as_text())
                    return redirect('change',  request.user.username)






