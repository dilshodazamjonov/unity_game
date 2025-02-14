from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Game, SystemRequirement, Comment, Profile, Ip, RatingStar, Rating
# Register your models here.

admin.site.register(Category)
# admin.site.register(Game)
admin.site.register(SystemRequirement)
admin.site.register(Profile)
admin.site.register(Ip)

admin.site.register(RatingStar)
admin.site.register(Rating)

class SystemInline(admin.TabularInline):
    fk_name = 'game'
    model = SystemRequirement
    extra = 1



@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title',  'category', 'get_count_views', 'created_at', 'get_photo')
    list_display_links = ('pk', 'title')
    list_filter = ('category',)
    inlines = [SystemInline]

    def get_photo(self, obj):
        if obj.image:
            try:
                return mark_safe(f'<img src="{obj.image.url}" width="75">')
            except:
                return '-'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'game', 'created_at')
    list_display_links = ('id', 'user')