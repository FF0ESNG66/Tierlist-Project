from django.db import models    
from django.contrib.auth.models import User
from django.utils.text import slugify


class CategoryModel(models.Model):
    category_tag_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_tag_name
    
    class Meta:
        verbose_name = 'categorymodel'
        verbose_name_plural = 'categorymodels'
        db_table = 'tagstable'
        ordering = ['category_tag_name']


class TemplateModel(models.Model):
    template_name = models.CharField(max_length=50, unique=True)
    template_category = models.ManyToManyField(CategoryModel, related_name='templates')
    template_description = models.TextField()
    urls_images = models.TextField()
    user = models.ForeignKey(User, to_field='username',on_delete=models.CASCADE)

    def __str__(self):
        return self.template_name

    class Meta:
        verbose_name = 'templateModel'
        verbose_name_plural = 'templatesModel'
        db_table = 'templatestable' 
        ordering = ['template_name']
    

class TierListModel(models.Model):
    tierlist_name = models.CharField(max_length=50, unique=True)
    s = models.TextField(null=True, blank=True)
    a = models.TextField(null=True, blank=True)
    b = models.TextField(null=True, blank=True)
    c = models.TextField(null=True, blank=True)
    d = models.TextField(null=True, blank=True)
    e = models.TextField(null=True, blank=True)
    fk_user = models.ForeignKey(User, to_field='username',on_delete=models.CASCADE)
    fk_template_name = models.ForeignKey(TemplateModel, to_field='template_name', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.tierlist_name

    class Meta:
        verbose_name = 'TierlistModel'
        verbose_name_plural = 'TierlistModels'
        db_table = 'tierlisttable'
        ordering = ['s', 'a', 'b', 'c', 'd', 'e']