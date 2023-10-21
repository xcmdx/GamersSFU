


import mimetypes
import rarfile  # pip install rarfile

from .models import *
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField


# форма поста игры
class PlaerGamePostForm(forms.ModelForm):

    Title = forms.CharField(max_length=255)
    Description = forms.CharField(max_length=255)
    

    GameFile = forms.FileField()
    GameIco = forms.FileField()

    class Meta:
        model = Game
        fields = ['Title', 'Description']

    def clean_image(self):
        data = self.cleaned_data
        
        if data.get('GameIco'):
            file_obj = data.getlist('GameIco')
            content_type = mimetypes.guess_type(file_obj[0])[0]
            if content_type not in  ['image/jpeg', 'image/png', 'image/gif']:
                raise ValidationError(f'GameIco File type not allowed ({content_type}).')
        
        if data.get('GameFile'):
            file_obj = data.getlist('GameFile')
            content_type = mimetypes.guess_type(file_obj[0])[0]
            if content_type.test_rarfile():
                raise ValidationError(f'GameFile File type not allowed ({content_type}).')

        return data

# форма жанров
class GameGanreForm(forms.Form):

    Genre = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(), 
        widget=forms.CheckboxSelectMultiple
    )
    
# форма загрузки нескольких изображений
class MultiImageForm(forms.Form):

    gameimages = MultiMediaField(
        min_num=1,
        max_num=5,
        max_file_size=1024*1024*5,
        media_type='image' 
    )
    
# вход
class LoginFrom(forms.Form):

    def __init__(self, *args, **kwargs):
        super(LoginFrom, self).__init__(*args, **kwargs)
        # for visible in self.visible_fields():
        #     visible.field.widget.attrs['class'] = 'form-control'

    Login = forms.CharField(
        max_length=255,
        label='логин'
    )

    password = forms.CharField(
        max_length=255,
        label='Введите пароль',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'введите пароль',
                'class': 'form-control'
            }
        )
    )


# регистрация
class RegForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        pass2 = self.cleaned_data['password1']
        pass1 = self.cleaned_data['password']
        if pass2 != pass1:
            raise ValidationError("пароли не совпадают 💢")

    class Meta:
        model = MyUsers
        fields = [ 'Login', 'email', 'password' ]

    password = forms.CharField(
        max_length = 255,
        label = 'Введите пароль',
        widget = forms.PasswordInput (
            attrs = {
                'placeholder' : 'введите пароль',
                'class' : 'form-control'
            }
        )
    )

    password1 = forms.CharField(
        max_length = 255,
        label = 'Повторите пароль',
        widget = forms.PasswordInput (
            attrs = {
                'placeholder' : 'повторите пароль',
                'class' : 'form-control'
            }
        )
    )
    

class SearchForm(forms.Form):

    search_field = forms.CharField( max_length=255, label="Поиск по названию")