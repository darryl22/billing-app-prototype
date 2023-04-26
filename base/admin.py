from django.contrib import admin
from .models import Utility, Reading, Profile

# Register your models here.

admin.site.register(Utility)
admin.site.register(Reading)
admin.site.register(Profile)