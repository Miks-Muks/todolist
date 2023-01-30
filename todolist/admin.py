from django.contrib import admin
from django.utils.translation import gettext_lazy

# Register your models here.

admin.site.site_header = gettext_lazy('Todo administration')
admin.site.site_title = gettext_lazy('Site admin')
