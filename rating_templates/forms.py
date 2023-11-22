from django import forms
from .models import TemplateModel,TierListModel


class TemplateForm(forms.ModelForm):
    class Meta:
        model = TemplateModel
        fields = ('template_name', 'template_category', 'template_description', 'urls_images')


class TierListForm(forms.ModelForm):
    class Meta:
        model = TierListModel
        fields = ('tierlist_name', 's', 'a', 'b', 'c', 'd', 'e')