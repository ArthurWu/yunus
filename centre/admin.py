from centre.models import *
from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    fields = ('menu','title','title_english','summary','summary_english', 'body','body_english', 'image')
    list_display = ('title', 'menu','created','modified')
    
    list_filter = ('menu',)
    
admin.site.register(Article, ArticleAdmin)

class MenuAdmin(admin.ModelAdmin):
    fields = ('name', 'name_english', 'parent', 'order', 'deletable')
    list_display = ('name', 'name_english', 'parent', 'order', 'deletable')
    list_filter = ('parent',)
    list_editable = ('name_english', 'order')

admin.site.register(Menu, MenuAdmin)

class HomePictureAdmin(admin.ModelAdmin):
	list_display = ('image', 'order')
	list_editable = ('order',)

admin.site.register(HomePicture, HomePictureAdmin)
admin.site.register(Subscription)