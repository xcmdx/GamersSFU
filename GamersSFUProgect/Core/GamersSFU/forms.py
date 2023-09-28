




from .models import ZipFile
from django import forms



# форма с загрузки zip файлов
class UploadZipForm(forms.ModelForm):
    file = forms.FileField()
    
    class Meta:
        model = ZipFile
        fields = ['file']
