# encoding: utf-8
from django.db import models

class Menu(models.Model):
    name = models.CharField(u'名称', max_length=50)
    name_english = models.CharField(u'英文名称', max_length=50)
    order = models.IntegerField(u'排序', blank=True, null=True)
    image = models.ImageField(u'图片', upload_to="menu", blank=True, null=True, help_text=u"图片大小为980px x 240px, 否则页面布局会出现不协调")
    parent = models.ForeignKey('Menu', verbose_name= u'父级', null=True, blank=True, related_name='menu_items')
    deletable = models.BooleanField(u'是否可删除', default=True)
    
    class Meta:
        verbose_name = u'菜单'
        verbose_name_plural= u'菜单'
    
    def __unicode__(self):
        return self.name

    def has_child(self):
        return Menu.objects.filter(parent__id=self.id)

class Article(models.Model):
    menu = models.ForeignKey(Menu, verbose_name= u'菜单栏', null=True, blank=True, related_name="articles")
    title = models.CharField(u'标题', max_length=200)
    title_english = models.CharField(u'英文标题', max_length=200)
    summary = models.TextField(u'概要')
    summary_english = models.TextField(u'英文概要')
    body = models.TextField(u'内容')
    body_english = models.TextField(u'英文内容')
    image = models.ImageField(u'图片', upload_to="articles", help_text=u"此图片是在文章列表是显示的，应该上传尺寸为 26px x 140px 或者相同比例的图片。否则显示的图片将出现不协调")
    created = models.DateTimeField(u'新建日期', auto_now_add=True)
    modified = models.DateTimeField(u'最后修改日期', auto_now=True)
    deletable = models.BooleanField(u'是否可删除', default=True)

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural= u'文章'
        
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/centre/article/%d' % self.id

class Subscription(models.Model):
    email = models.EmailField(u'邮箱')

    class Meta:
        verbose_name = u'订阅'
        verbose_name_plural= u'订阅'
        
    def __unicode__(self):
        return self.email

class HomePicture(models.Model):
    image = models.ImageField(upload_to="home", verbose_name=u"图片", help_text=u"图片大小为980px x 512px, 否则页面布局会出现不协调")
    articles = models.OneToOneField(Article, null=True, blank=True, verbose_name=u'关联文章', help_text=u"多张图片不能同时关联到同一篇文章，图片和文章是一一对应的关系")
    order = models.IntegerField(u"排序", blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.image

    class Meta:
        verbose_name = u'首页轮播图片'
        verbose_name_plural= u'首页轮播图片'
