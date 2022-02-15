from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import cable
from .models import sub
from .models import load
from .models import pillar

admin.site.register(cable, LeafletGeoAdmin)
admin.site.register(sub, LeafletGeoAdmin)
admin.site.register(load, LeafletGeoAdmin)
admin.site.register(pillar, LeafletGeoAdmin)
