# encoding: utf-8
from django.contrib.syndication.views import Feed
from centre.models import Article

class LatestArticleFeed(Feed):
    title = u"最新文章"
    link = "/latest/feed/"
    description = "最新文章"

    def items(self):
        return Article.objects.order_by('-created')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary