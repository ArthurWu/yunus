from centre.models import Menu

def menus(request):
	menus = Menu.objects.filter(parent=None).order_by('order')
	return {'menus': menus}