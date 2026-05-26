from django.contrib import admin
from .models import Lake, LakePhoto


class LakePhotoInline(admin.TabularInline):
    model = LakePhoto
    extra = 1


@admin.register(Lake)
class LakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'pollution_level', 'area_sq_km')
    list_filter = ('pollution_level',)
    search_fields = ('name', 'location')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [LakePhotoInline]


@admin.register(LakePhoto)
class LakePhotoAdmin(admin.ModelAdmin):
    list_display = ('lake', 'photo_type', 'caption', 'uploaded_at')
    list_filter = ('photo_type', 'lake')
