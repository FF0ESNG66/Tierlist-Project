from django.shortcuts import render
from rating_templates.models import TemplateModel, TierListModel


def tierlist_single_view(request, tierlist_name):
    if request.method == 'GET':
        tierlist = TierListModel.objects.get(tierlist_name=tierlist_name)
        if tierlist:
            tierlist_id = tierlist.id
            tags = list(tierlist.fk_template_name.template_category.values_list('category_tag_name', flat=True))
            context = {
                'name': tierlist.tierlist_name,
                'tags': ', '.join(tags),
                'S_Field': tierlist.s.split(','),
                'A_Field': tierlist.a.split(','),
                'B_Field': tierlist.b.split(','),
                'C_Field': tierlist.c.split(','),
                'D_Field': tierlist.d.split(','),
                'E_Field': tierlist.e.split(','),
                'owner': tierlist.fk_user,
                'id': tierlist_id,
            }
            return render(request, 'rates_lobby/tierlist_single.html', context=context)
        else:
            context = {
                'tierlists': 'No tierlists to show'
            }
            return render(request, 'rates_lobby/tierlist_single.html', context=context)



def tierlist_list_view(request):
    if request.method == 'GET':
        tierlists = TierListModel.objects.all()
        content = []
        if tierlists:
            for tierlist in tierlists:
                tierlist_id = tierlist.id
                image_pool = tierlist.s.split(',')
                cover_image = image_pool[0]
                print(cover_image)
                tags = list(tierlist.fk_template_name.template_category.values_list('category_tag_name', flat=True))
                data = {
                    'name': tierlist.tierlist_name,
                    'tags': ', '.join(tags),
                    'cover_image': cover_image,
                    'owner': tierlist.fk_user,
                    'id': tierlist_id,
                }
                content.append(data)
            context = {
                'tierlists': content,
            }
            return render(request, 'rates_lobby/tierlist_list.html', context=context)
        else:
            context = {
                'tierlists': tierlists
            }
            return render(request, 'rates_lobby/tierlist_list.html', context=context)



def templates_list_view(request):
    if request.method == 'GET':
        templates = TemplateModel.objects.all()
        content = []
        if templates:
            for template in templates:
                tags = list(template.template_category.values_list('category_tag_name', flat=True))
                images_urls = template.urls_images.split(',')
                data = {
                   'template_name':template.template_name,
                   'template_category': (', ').join(tags),
                   'template_description': template.template_description,
                   'urls_images': images_urls,
                   'id': template.id,
                   'owner':template.user,
                   'current_user': request.user.username,
                }
                content.append(data)
            context = {
                'templates': content,
                }
            return render(request, 'rates_lobby/templates_list.html', context=context)
        else:
            context = {
                'templates': templates,
            }
            return render(request, 'rates_lobby/templates_list.html', context=context)

   

def lobby(request):
    templates_number = TemplateModel.objects.all().count()
    tierlists_number = TierListModel.objects.all().count()
    if request.method == 'GET':
        tierlists = TierListModel.objects.all()
        content = []
        if tierlists:
            for tierlist in tierlists:
                tierlist_id = tierlist.id
                description = tierlist.fk_template_name.template_description
                tags = list(tierlist.fk_template_name.template_category.values_list('category_tag_name', flat=True))
                data = {
                    'name': tierlist.tierlist_name,
                    'tags': ', '.join(tags),
                    'description': description,
                    'S_Field': tierlist.s.split(','),
                    'A_Field': tierlist.a.split(','),
                    'B_Field': tierlist.b.split(','),
                    'C_Field': tierlist.c.split(','),
                    'D_Field': tierlist.d.split(','),
                    'E_Field': tierlist.e.split(','),
                    'owner': tierlist.fk_user,
                    'id': tierlist_id,
                }
                content.append(data)
            context = {
                'tierlists': content,
                'total_templates': templates_number,
                'total_tierlists': tierlists_number,
            }
            return render(request, 'rates_lobby/home.html', context=context)
        else:
            context = {
                'tierlists': tierlists
            }
            return render(request, 'rates_lobby/home.html', context=context)



def about(request):
    return render(request, 'rates_lobby/about.html')
