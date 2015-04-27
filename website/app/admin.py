from django.contrib import admin

from .models import NewsHeadline

admin.site.register(NewsHeadline)

from .models import Price

admin.site.register(Price)