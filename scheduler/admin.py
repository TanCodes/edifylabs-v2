from django.contrib import admin
from .models import ScheduleClients
# Register your models here.


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('first_name_S', 'last_name_S',
                    'coaching_type_course', 'review_call')


admin.site.register(ScheduleClients, ScheduleAdmin)
