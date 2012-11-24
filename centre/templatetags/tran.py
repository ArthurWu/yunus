from django import template

register = template.Library()

def tran(obj, field, lang_cod):
	field += '' if lang_cod == 'zh-cn' else '_english'
	return getattr(obj, field)

register.simple_tag(tran)
