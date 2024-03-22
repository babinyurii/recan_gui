from django.contrib import admin
from .models import SessionData, Session



class SessionDataAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'alignment', 'align_len',
                    'dist_method', )

admin.site.register(SessionData, SessionDataAdmin)
admin.site.register(Session)
