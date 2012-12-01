# encoding: utf-8
from centre.models import *
from django.contrib import admin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.admin.actions import delete_selected as _delete_selected
import utils

class ArticleAdmin(admin.ModelAdmin):
	fields = ('menu','title','title_english','summary','summary_english', 'body','body_english', 'image')
	list_display = ('title', 'menu','created','modified')
	list_filter = ('menu',)
	actions = ['delete_selected',]

	class Media:
		js = (
			'tiny_mce/tiny_mce.js',
			'script/textareas.js'
		)

	def delete_selected(self, request, queryset):
		cannot_delete = [obj for obj in queryset if not obj.deletable]
		if cannot_delete:
			from django.contrib import messages
			messages.add_message(request, messages.ERROR, u'您选择中的，“%s”是网站固定的网站内容，不能删除！' % ','.join(i.title for i in queryset))
			return redirect('/admin/centre/article/')

		return _delete_selected(self, request, queryset)

admin.site.register(Article, ArticleAdmin)

class MenuAdmin(admin.ModelAdmin):
	fields = ('name', 'name_english', 'parent', 'image', 'order')
	list_display = ('name', 'name_english', 'parent', 'order', 'deletable')
	list_filter = ('parent',)
	list_editable = ('name_english', 'order')
	actions = ['delete_selected',]

	def delete_selected(self, request, queryset):
		cannot_delete = [obj for obj in queryset if not obj.deletable]
		if cannot_delete:
			from django.contrib import messages
			messages.add_message(request, messages.ERROR, u'您选择中的菜单中，“%s”为内置菜单，不能删除！' % ','.join([i.name for i in queryset]))
			return redirect('/admin/centre/menu/')

		return _delete_selected(self, request, queryset)

admin.site.register(Menu, MenuAdmin)

class HomePictureAdmin(admin.ModelAdmin):
	list_display = ('image', 'order')
	list_editable = ('order',)

admin.site.register(HomePicture, HomePictureAdmin)

def send_emails(modeladmin, request, queryset):
	opts = modeladmin.model._meta
	app_label = opts.app_label
	title = u"发送邮件给订阅用户"
	email = utils.get_email_info()
	return render(request, 'send_email_confirmation.html', locals())
	
send_emails.short_description = u'发送邮件'

class SubscriptionAdmin(admin.ModelAdmin):
	actions = [send_emails,]

admin.site.register(Subscription, SubscriptionAdmin)