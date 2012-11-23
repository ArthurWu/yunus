# encoding: utf-8
from centre.models import *
from django.contrib import admin
from django.shortcuts import render
from django.core.mail import EmailMessage
import logging

logger = logging.getLogger(__name__)

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

class SubscriptionAdmin(admin.ModelAdmin):
	actions = ['send_email']

	def send_email(self, request, queryset):
		opts = self.model._meta
		app_label = opts.app_label
		logger.debug('send email ...')
		#send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None)
		if request.POST.get('post'):
			subject = request.POST.get('title', '')
			body = request.POST.get('body', '')
			from_email = '175040128@qq.com'
			recipient_list = [i.email for i in queryset]
			attachment = request.FILES['attachment']
			msg = EmailMessage(subject, body, from_email, recipient_list)
			msg.attach('file.jpg', attachment)#, mimetype)
			try:
				msg.send()
			except Exception:
				return HttpResponse('邮件发送失败！')
			return HttpResponse('邮件发送成功！')

		title = u"发送邮件给订阅用户"

		return render(request, 'send_email_confirmation.html', locals())
		
	send_email.short_description = u'发送邮件'

admin.site.register(Subscription, SubscriptionAdmin)