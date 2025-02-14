from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Game, SystemRequirement, Comment, Profile


# Форма для входа в Аккаунт
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите логин'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))


# Форма для регистрации
class RegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль'
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите логин'
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите фамилию'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите почту'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')




class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('title', 'content', 'image', 'video', 'category')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название игры'
            }),

            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание игры'
            }),

            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),

            'video': forms.FileInput(attrs={
                'class': 'form-control'
            }),

            'category': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class SystemForm(forms.ModelForm):
    class Meta:
        model = SystemRequirement
        fields = ['op_system', 'processor', 'ram', 'video_card', 'memory']
        widgets = {
            'op_system': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Операционная система'
            }),

            'processor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Процессор'
            }),

            'ram': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Оперативная память'
            }),

            'video_card': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Видео карта'
            }),

            'memory': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пямать (размер)'
            }),

        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ввидите текст'
            })
        }


class EditAccountFrom(UserChangeForm):
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))

    old_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'old_password', 'new_password', 'confirm_password')


class EditProfileForm(forms.ModelForm):
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    about = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    avatar = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Profile
        fields = ('city', 'about', 'avatar')






