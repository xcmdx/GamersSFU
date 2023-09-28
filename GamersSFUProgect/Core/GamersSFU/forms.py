


from django.core import validators

from django.core.exceptions import ValidationError

from .models import *
from django import forms




class PlaerGamePostForm(forms.ModelForm):

    Title = forms.CharField(max_length=255)
    Description = forms.CharField(max_length=255)
    
    class Meta:
        model = Game
        fields = ['Title', 'Description']


# форма загрузки нескольких изображений
class MultiImageForm(forms.Form):
    
    images = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def clean_files(self):
        files = self.cleaned_data['files']
        if not files:
            raise ValidationError('Please select at least one file.')
        return files


# форма загрузки zip файлов игры
class GameFileForm(forms.ModelForm):
    class Meta:
        model = ZipFile
        fields = [ 'GameFile' ]


    

