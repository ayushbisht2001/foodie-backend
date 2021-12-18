from django.contrib import admin

from .models import Address, Cuisines, Restaurant

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Cuisines)
admin.site.register(Address)