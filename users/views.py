from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.urls import reverse
from .forms import LoginForm, RegisterForm, EditProfileForm, ChangeEmailForm
from .tokens import account_activation_token, email_change_token
from rating_templates.models import TierListModel, TemplateModel

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from rating_templates.forms import TierListForm, TemplateForm
import re





def ChangeEmailConfirmation(request, username, uidb64, token):
    User_Func = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User_Func.objects.get(pk=uid)
    except:
        user = None

    if user is not None and email_change_token.check_token(user, token):
        if request.method == 'GET':
            form = ChangeEmailForm()
            context = {
                'form': form
            }
            return render(request, 'users/change_email_template.html', context=context)
        elif request.method == 'POST':
            current_user = request.user
            email = request.POST.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already taken by other user.')
                return redirect(reverse('users:change_email_mail', args=[username, uid, token]))
            else:
                current_user.email = email
                current_user.save()
                messages.success(request, 'Your email address has been changed successfull')
                return redirect(reverse('users:profile', args=[username]))
    else:
        messages.error(request, f"Activation link is invalid!{token}")
    return redirect(reverse("rates_lobby:home"))



@login_required
def ChangeEmailMail(request, username):
    user_instance = User.objects.get(username=username)
    token = email_change_token.make_token(user_instance)
    print(f'Generated Token: {token}')
    mail_subject = "Change Email Address Confirmation."
    message =  render_to_string("users/email_change_mail.html", {
        'user': user_instance.username,
        'domain': get_current_site(request).domain,
        'username': username,
        'uid': urlsafe_base64_encode(force_bytes(user_instance.pk)),
        'token': token,
        'Protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[user_instance.email])
    if email.send():
        messages.success(request, f'Dear {user_instance.username}, please go to {user_instance.email} inbox and click on \
                        received confirmation link in order to change your email address. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {user_instance.email}. Check if you typed it correctly.')



@login_required()
def change_email_view(request, username):
    if request.method == 'GET':
        current_user = User.objects.get(username=username)
        username = current_user.username
        ChangeEmailMail(request, username)
        return redirect(reverse(f'users:profile', args=[username]))



@login_required()
def profile_view(request, username):
    user = User.objects.get(username=username)
    if request.method == 'GET':
        templates = TemplateModel.objects.filter(user__username=username).count()
        tierlists = TierListModel.objects.filter(fk_user__username=username).count()
        context = {
            'tierlists': tierlists,
            'templates': templates,
            'user': user,
            'current_user': request.user,
        }
        print(f"Current User: {request.user}")
        print(f"Current User ID: {request.user.id}")
        return render(request, 'users/profile.html', context=context)



@login_required()
def edit_profile_view(request, username):
    if request.method == 'GET':
        user = User.objects.get(username=username)
        form = EditProfileForm(instance=user)
        context = {'form': form}
        return render(request, 'users/edit_profile.html', context)
    elif request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, f'Data updated successfully')
            return redirect(reverse('rates_lobby:home'))
        else:
            messages.error(request, f"Something's wrong in the data provided")
            return redirect(reverse('users:edit_profile'))



def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thanks for your email confirmation. Now you can login your account")
        return redirect(reverse("users:login"))
    else:
        messages.error(request, "Activation link is invalid!")
    return redirect(reverse("rates_lobby:home"))



def activateEmail(request, user):
    mail_subject = "Activate your user account"
    message =  render_to_string("users/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'Protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[user.email])
    if email.send():
        messages.success(request, f'Dear {user.first_name + " " + user.last_name}, please go to {user.email} inbox and click on \
                        received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {user.email}. Check if you typed it correctly.')



def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})
    
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Sorry, this email is already in use. Use another one.')
            return redirect(reverse('users:register'))
        else: 
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.first_name = user.first_name.capitalize()
                user.last_name = user.last_name.capitalize()
                user.email = user.email.lower()
                user.is_active = False
                user.save()  # check this, beware
                activateEmail(request, user)
                return redirect(reverse('rates_lobby:home'))
            else:
                return render(request, 'users/register.html', {'form': form})



def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(reverse('rates_lobby:about'))
        
        form = LoginForm()
        context = {
            'form':form,
        }

        return render(request, 'users/login.html', context=context)
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
    
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request,username=username,password=password)
        if user:
            login(request, user)
            messages.success(request,f'Hi {username.title()}, welcome back!')
            return redirect(reverse('rates_lobby:home'))
    
    # form is not valid or user is not authenticated
    messages.error(request,f'Invalid username or password')
    return render(request,'users/login.html',{'form': form})



@login_required
def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect(reverse('users:login'))



@method_decorator(login_required, name='dispatch')
class TierlistOwned(DetailView):
    def get(self, request, username):
        tierlists_array = []
        user = User.objects.get(username=username)
        user_tierlist = TierListModel.objects.filter(fk_user=user.username)
        for tierlist in user_tierlist:
            image_pool = tierlist.s.split(',')
            cover_image = image_pool[0]
            tags = list(tierlist.fk_template_name.template_category.values_list('category_tag_name', flat=True))
            data = {
                'name': tierlist.tierlist_name,
                'tags': ', '.join(tags),
                'description': tierlist.fk_template_name.template_description,
                'current_user': request.user,
                'cover_image': cover_image,
                'owner': user,
                'id': tierlist.id,
            }
            tierlists_array.append(data)
        context = {
            'tierlists': tierlists_array
        }
        print(f'Current user: {request.user}')
        print(f'owner: {user.username}')
        return render(request, 'users/tierlist_profile.html', context=context)



@login_required
def Tierlist_View_Single(request, username, tierlist_name):
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
                'owner': username,
                'id': tierlist_id,
            }
            return render(request, 'users/tierlist_single.html', context=context)
        else:
            context = {
                'tierlists': 'No tierlists to show'
            }
            return render(request, 'users/tierlist_single.html', context=context)



@login_required
def DeleteTierlist_Profile(request, username, id):
    user = User.objects.get(username=username)
    query = TierListModel.objects.filter(fk_user=user.username)
    tierlist = get_object_or_404(query, id=id)
    tierlist_name = tierlist.fk_template_name

    if request.method == 'GET':
        context = {
            'name': tierlist_name,
            'username': user.username,
        }
        return render(request, 'users/delete_tierlist_profile.html', context=context)
    elif request.method == 'POST':
        tierlist.delete()
        messages.success(request, 'Your tierlist has been deleted successfully.')
        return redirect(reverse('users:tierlist-owned', args=[username]))
    


@login_required
def EditTierlist_Profile(request, username, id):
    user = User.objects.get(username=username)
    query = TierListModel.objects.filter(fk_user=user.username)
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
            'username': user.username,
            'id':tierlist.id,
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
            return redirect(reverse('users:tierlist-owned', args=[username]))
        else:
            messages.error(request, 'Something went wrong in the process of editing your tierlist, please, try again.')
            return redirect(reverse('users:tierlist-owned', args=[username]))
        


@method_decorator(login_required, name='dispatch')
class TemplatesOwned(DetailView):
    def get(self, request, username):
        user = User.objects.get(username=username)
        user_templates = TemplateModel.objects.filter(user=user.username)
        content = []
        if user_templates:
            for template in user_templates:
                tags = list(template.template_category.values_list('category_tag_name', flat=True))
                images_urls = template.urls_images.split(',')
                data = {
                'template_name':template.template_name,
                'template_category': (', ').join(tags),
                'template_description': template.template_description,
                'username': user,
                'current_user': request.user,
                'urls_images': images_urls,
                'id': template.id,
                }
                content.append(data)
            context = {
                'templates': content,
                }
            return render(request, 'users/templates_profile.html', context=context)
        else:
            context = {
                'templates': user_templates,
            }
            return render(request, 'users/templates_profile.html', context=context)



@login_required
def EditTemplates_Profile(request, username, id):
    current_user = User.objects.get(username=username)
    query = TemplateModel.objects.filter(user=current_user.username)
    template = get_object_or_404(query, id=id)
    if request.method == 'GET':
        template_form = TemplateForm(instance=template)
        context = {
            'form': template_form
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
                return redirect(reverse('users:templates-owned', args=[username]))
            else:
                messages.error(request, "Something went wrong editing the template, please, try again.")
                return redirect(reverse('users:templates-owned', args=[username]))
        else:
            messages.error(request, 'Sorry, you must authenticate your account before doing any template.')
            return redirect(reverse('users:login'))
        


@login_required
def DeleteTemplates_Profile(request, username, id):
    current_user = User.objects.get(username=username)
    query = TemplateModel.objects.filter(user=current_user.username)
    template = get_object_or_404(query, id=id)

    if request.method == 'GET':
        context = {
            'name': template.template_name,
            'username': current_user.username
        }
        return render(request, 'users/delete_template_profile.html', context=context)
    elif request.method == 'POST':
        template.delete()
        messages.success(request, 'Your template has been deleted successfully.')
        return redirect(reverse('users:templates-owned', args=[username]))