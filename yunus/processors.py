from centre.models import Menu
from centre.utils import read_links

def menus(request):
	menus = Menu.objects.filter(parent=None).order_by('order')
	return {'menus': menus, 'links': read_links()}