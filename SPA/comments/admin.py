from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# root 123
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_html_photo', 'user_name', 'user_email')
    list_display_links = ('id',)
    readonly_fields = ('get_html_photo',)

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = 'Miniature'

    def user_name(self, obj):
        return obj.user.username

    user_name.short_description = 'Username'

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'level', 'author', 'body', 'created_time', 'parent')
    list_display_links = ('id',)
    search_fields = ('body',)
    list_editable = ('author',)
    list_filter = ('created_time', 'file', 'image', 'parent')
    readonly_fields = ['created_time']

    def add_view(self, request, form_url='', extra_context=None):
        self.fields = ('body', 'image', 'file', 'parent')
        return super().add_view(request, form_url=form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        # set the current user as the author of the comment
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile, ProfileAdmin)
