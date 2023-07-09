from django.contrib import admin

# Register your models here.
from .models import Profile, Section, Price, Features, Landing

admin.site.register(Profile)
admin.site.register(Section)


class FeaturesAdmins(admin.StackedInline):
    model = Features
    extra: int = 1
    fields = ('title', )

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('title', 'sub_title')
    inlines = [FeaturesAdmins]


@admin.register(Features)
class FeaturesAdmin(admin.ModelAdmin):
    list_display = ('title', 'to')


admin.site.register(Landing)