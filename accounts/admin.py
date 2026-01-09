from django.contrib import admin
from .models import CustomUser
from django.utils.html import format_html

# Register your models here.

admin.site.site_header = "Job Portal Admin"
admin.site.site_title = "Job Portal Admin Portal"
admin.site.index_title = "Welcome to Job Portal Admin"

class AdminCSS(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('admin/custom_admin.css',)
        }


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('profile_image_tag', 'email', 'full_name', 'roles', 'phone', 'is_staff', 'is_active')
    search_fields = ('email','full_name')
    list_filter = ('roles', 'is_active')

    def profile_image_tag(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />',
                               obj.profile_image.url)
        return "No Image"

# itizamritamishra@gmail.com = "hirenexus@123"   student
# ankit@gmail.com = "django2025"                 recruiter
# amrita@gmail.com = "admin"                     admin