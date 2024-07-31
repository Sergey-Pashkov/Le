from django import forms
from .models import Functions_of_performers

class FunctionsOfPerformersForm(forms.ModelForm):
    class Meta:
        model = Functions_of_performers
        fields = ['name', 'description', 'owner']
