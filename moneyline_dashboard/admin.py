from django.contrib import admin

# Register your models here.

from .models import SportsEvent,BettingLine

admin.site.register(SportsEvent)
admin.site.register(BettingLine)
