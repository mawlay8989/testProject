from django import forms
from .models import Category

class AddTaskForm(forms.Form):
    titre = forms.CharField()

    CHOICES = Category.objects.all().values_list('id', 'name')

    category = forms.ModelChoiceField(queryset=Category.objects.all())
    description = forms.CharField(widget=forms.Textarea)

class AddCategoryForm(forms.Form):
    name = forms.CharField()
