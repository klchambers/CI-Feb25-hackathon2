from django.contrib import admin
from .models import Event, EventCategory

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'price', 'spots_remaining', 'is_active')
    list_filter = ('category', 'is_active', 'city', 'state')
    search_fields = ('title', 'description', 'location_name')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date'
    list_editable = ('is_active', 'spots_remaining')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'category', 'image')
        }),
        ('Event Details', {
            'fields': ('date', 'duration', 'price', 'capacity', 'spots_remaining')
        }),
        ('Location', {
            'fields': ('location_name', 'address', 'city', 'state', 'zip_code')
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )