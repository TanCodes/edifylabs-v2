from django.contrib import admin
from .models import Course, Clients


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'date')


class ClientsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',
                    'coaching_type_course', 'email_id')


admin.site.register(Course, CourseAdmin)
admin.site.register(Clients, ClientsAdmin)
