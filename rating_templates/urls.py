from django.urls import path
from rating_templates import views

app_name = "rating_templates"

urlpatterns = [
    path('template/', views.TemplateView.as_view(), name="template-creation"),
    path('tierlist/<str:template_name>', views.TierListView.as_view(), name='tierlist-creation'),
    path('tierlist/edit/<int:id>', views.EditTierlist, name='edit-tierlist'),
    path('tierlist/delete/<int:id>', views.DeleteTierlist, name='delete-tierlist'),
    path('template/edit/<int:id>', views.EditTemplates, name='edit-templates'),
    path('template/delete/<int:id>', views.DeleteTemplates, name='delete-templates')
]