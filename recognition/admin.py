from django.contrib import admin
from django.utils.html import format_html
from .models import Person, PhoneUsageDetection

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(PhoneUsageDetection)
class PhoneUsageDetectionAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'detected_at', 'phone_users_count', 'person_count', 'phone_count']
    list_filter = ['detected_at', 'phone_users_count']
    search_fields = ['description']
    readonly_fields = ['image_preview_large', 'detected_at', 'person_count', 'phone_count', 'phone_users_count']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="75" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 800px; height: auto;" />', obj.image.url)
        return "No Image"
    image_preview_large.short_description = 'Detection Image'

    fieldsets = (
        ('Detection Image', {
            'fields': ('image_preview_large',)
        }),
        ('Detection Details', {
            'fields': ('detected_at', 'person_count', 'phone_count', 'phone_users_count', 'description')
        }),
    )
