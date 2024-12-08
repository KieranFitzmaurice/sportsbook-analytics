from django.contrib import admin

# Register your models here.

from .models import SportsEvent,BettingLine,Portfolio,Wager

admin.site.register(SportsEvent)
admin.site.register(BettingLine)
admin.site.register(Portfolio)
admin.site.register(Wager)
