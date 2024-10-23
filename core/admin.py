from django.contrib import admin
from .models import *

class BetAdmin(admin.ModelAdmin):
    list_display=["id","user","result","date_time"]

    search_fields=["result","date_time"]

admin.site.register(Bet, BetAdmin)



class HistoryAdmin(admin.ModelAdmin):
    list_display=["id","user","last_modified",]


admin.site.register(History, HistoryAdmin)