from django.forms import ModelChoiceField
from django.contrib import admin

from .models import *



class AdminBook(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='books'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AdminAudioBook(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='audiobooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AdminPodcast(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='podcasts'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Book, AdminBook)
admin.site.register(Audiobook, AdminAudioBook)
admin.site.register(Podcast, AdminPodcast)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Customer)