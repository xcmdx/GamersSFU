



from .models import *
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField


# форма поста игры
class PlaerGamePostForm(forms.ModelForm):

    Title = forms.CharField(max_length=255)
    Description = forms.CharField(max_length=255)
    
    class Meta:
        model = Game
        fields = ['Title', 'Description']


# форма загрузки нескольких изображений
class MultiImageForm(forms.Form):
    
    # images = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))


    # If you need to upload media files, you can use this:
    gameimages = MultiMediaField(
        min_num=1,
        max_num=5,
        max_file_size=1024*1024*5,
        media_type='image'  # 'audio', 'video' or 'image'
    )
    
    # def clean_files(self):
    #     files = self.cleaned_data['files']
    #     if not files:
    #         raise ValidationError('Please select at least one file.')
    #     return files


# форма загрузки zip файлов игры
class GameFileForm(forms.ModelForm):
    class Meta:
        model = ZipFile
        fields = [ 'GameFile' ]


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
class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
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