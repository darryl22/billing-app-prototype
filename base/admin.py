from django.contrib import admin
from .models import Utility, Reading, Profile, Invoice, Contract, Receipt

# Register your models here.

admin.site.register(Utility)
admin.site.register(Reading)
admin.site.register(Profile)
admin.site.register(Invoice)
admin.site.register(Contract)
admin.site.register(Receipt)