from django.shortcuts import render
from django.views.generic import CreateView, FormView
from .forms import TemplateForm, TierListForm
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import TemplateModel, TierListModel
from django.contrib.auth.decorators import login_required
import re



class TemplateView(CreateView):
    form_class = TemplateForm
    template_name = 'rating_templates/template_creation.html'
    success_url = 'rates_lobby:home'

    def post(self, request, *args, **kwargs):
        form = TemplateForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                form_instance = form.instance
                form_instance.template_name = form.instance.template_name.lower()
                current_user = request.user
                form_instance.user_id = current_user
                form.save()
                messages.success(request, 'Template created successfully.')
                return redirect(reverse('rates_lobby:home'))
            else:
                messages.error(request, "Something went wrong creating the template, please, try again.")
                return redirect(reverse('rating_templates:template-creation'))
        else:
            messages.error(request, 'Sorry, you must authenticate your account before doing any tierlist.')
            return redirect(reverse('rates_lobby:home'))


        

class TierListView(CreateView):

    def get(self, request, template_name, *args, **kwargs):
        form = TierListForm
        template_instance = get_object_or_404(TemplateModel.objects.filter(template_name=template_name))
        if template_instance:
            categories_qs = template_instance.template_category.values_list('category_tag_name', flat=True) 
            categories_list = list(categories_qs)
            categories_str = ', '.join(categories_list)
            context = {
                'form': form,
                'template_name': template_instance.template_name,
                'template_tags': categories_str, 
                'images': template_instance.urls_images.split(',')
            }
            return render(request, 'rating_templates/tier_list.html', context=context)


    def post(self, request, *args, **kwargs):
        form = TierListForm(request.POST)
        tiers = ['s', 'a', 'b', 'c', 'd', 'e']
        current_user = request.user
        template_name = request.POST.get('fk_template_name')
        template_instance = get_object_or_404(TemplateModel, template_name=template_name)
        if current_user.is_authenticated:
            if form.is_valid():
                form_instance = form.save(commit=False)
                form_fields_as_dict = form.cleaned_data
                print(form_fields_as_dict)
                for field_name, field_value in form_fields_as_dict.items():
                    if field_name not in tiers:
                        continue
                    if isinstance(field_value, str):
                        urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|gif|bmp)', field_value)
                        # r'https?://\S+?\.(?:png|jpg|jpeg|gif|bmp)'   This was the previous regular expression I was using
                        # new r'https?://[^\s/$.?#].[^\s]*'
                        #another: r'https?://\S+'
                        setattr(form_instance, field_name, ','.join(urls))
                form_instance.fk_user = current_user 
                form_instance.fk_template_name = template_instance
                form_instance.save()
                messages.success(request, 'Your tierlist has been created successfully.')
                return redirect(reverse('rates_lobby:home'))
            else:
                messages.error(request, 'Something went wrong while creating your tierlist, please, try again.')
                return redirect(reverse('rating_templates:tierlist-creation'))
        else:
            messages.error(request, 'Sorry, you must authenticate your account before doing any tierlist.')
            return redirect(reverse('rates_lobby:home'))



@login_required
def EditTierlist(request, id):
    query = TierListModel.objects.filter(fk_user=request.user)
    tierlist = get_object_or_404(query, id=id)
    template_name = tierlist.fk_template_name
    template_instance = TemplateModel.objects.get(template_name=template_name)
    tags = list(template_instance.template_category.values_list('category_tag_name', flat=True))
    images = template_instance.urls_images
    if request.method == 'GET':
        context = {
            'form': TierListForm(instance=tierlist),
            'template_name': template_name,
            'template_tags': ', '.join(tags),
            'images': images.split(','),
            'id':tierlist.id
        }
        return render(request, 'rating_templates/tier_list.html', context=context)
    elif request.method == 'POST':
        edited_tierlist = TierListForm(request.POST, instance=tierlist)
        if edited_tierlist.is_valid():
            tierlist_instance = edited_tierlist.save(commit=False)
            edited_data = edited_tierlist.cleaned_data
            for field_name, field_value in edited_data.items():
                if isinstance(field_value, str):
                    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|gif|bmp)', field_value)
                    # r'https?://\S+?\.(?:png|jpg|jpeg|gif|bmp)'   This was the pre vious regular expression I was using
                    # new r'https?://[^\s/$.?#].[^\s]*'
                    # pls r'https?://\S+?(?=(https?://|$))'
                    setattr(tierlist_instance, field_name, ','.join(urls))
            tierlist_instance.save()
            messages.success(request, 'Your tierlist has been updated successfully!.')
            return redirect(reverse('rates_lobby:home'))
        else:
            messages.error(request, 'Something went wrong in the process of editing your tierlist, please, try again.')
            return redirect(reverse('rates_lobby:home'))
        


@login_required
def DeleteTierlist(request, id):
    query = TierListModel.objects.filter(fk_user=request.user)
    tierlist = get_object_or_404(query, id=id)
    tierlist_name = tierlist.fk_template_name

    if request.method == 'GET':
        context = {
            'name': tierlist_name,
        }
        return render(request, 'rating_templates/delete_tierlist.html', context=context)
    elif request.method == 'POST':
        tierlist.delete()
        messages.success(request, 'Your tierlist has been deleted successfully.')
        return redirect(reverse('rates_lobby:home'))
    


@login_required
def EditTemplates(request, id):
    query = TemplateModel.objects.filter(user=request.user)
    template = get_object_or_404(query, id=id)
    if request.method == 'GET':
        template_form = TemplateForm(instance=template)
        context = {
            'form': template_form,
            'id': id
        }
        return render(request, 'rating_templates/template_creation.html', context=context)
    elif request.method == 'POST':
        form = TemplateForm(request.POST, instance=template)
        if request.user.is_authenticated:
            if form.is_valid():
                form_instance = form.instance
                form_instance.template_name = form.instance.template_name.lower()
                current_user = request.user
                form_instance.user_id = current_user
                form.save()
                messages.success(request, 'Template edited successfully.')
                return redirect(reverse('rates_lobby:home'))
            else:
                messages.error(request, "Something went wrong editing the template, please, try again.")
                return redirect(reverse('rates_lobby:home'))
        else:
            messages.error(request, 'Sorry, you must authenticate your account before doing any template.')
            return redirect(reverse('users:login'))
        


@login_required
def DeleteTemplates(request, id):
    query = TemplateModel.objects.filter(user=request.user)
    template = get_object_or_404(query, id=id)

    if request.method == 'GET':
        context = {
            'name': template.template_name,
        }
        return render(request, 'rating_templates/delete_template.html', context=context)
    elif request.method == 'POST':
        template.delete()
        messages.success(request, 'Your template has been deleted successfully.')
        return redirect(reverse('rates_lobby:home'))