from django.contrib import admin
from .models import Medicaments, Interaction


# Register your models here.
admin.site.register(Medicaments)
admin.site.register(Interaction)