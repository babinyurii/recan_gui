from django.contrib import admin
from app_recan_gui.models import SessionData, Session



class SessionDataAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'alignment', 'align_len',
                   'dist_method', )
    readonly_fields = [field.name for field in SessionData._meta.get_fields()]            

admin.site.register(SessionData, SessionDataAdmin)
admin.site.register(Session)
