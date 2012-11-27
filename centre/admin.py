# encoding: utf-8
from centre.models import *
from django.contrib import admin
from django.shortcuts import render

class ArticleAdmin(admin.ModelAdmin):
    fields = ('menu','title','title_english','summary','summary_english', 'body','body_english')
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
    #list_display = ('order',)
    #list_editable = ('order',)
    pass

admin.site.register(HomePicture, HomePictureAdmin)

def send_emails(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    app_label = opts.app_label
    title = u"发送邮件给订阅用户"
    return render(request, 'send_email_confirmation.html', locals())
    
send_emails.short_description = u'发送邮件'

class SubscriptionAdmin(admin.ModelAdmin):
    actions = [send_emails,]

admin.site.register(Subscription, SubscriptionAdmin)