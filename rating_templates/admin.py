from django.contrib import admin
from .models import *
from django import forms

class TemplateModelForm(forms.ModelForm):
    class Meta:
        model = TemplateModel
        fields = '__all__'
        widgets = {
            'template_category': forms.CheckboxSelectMultiple,
        }


admin.site.register(TemplateModel)
admin.site.register(TierListModel)

admin.site.register(CategoryModel)
