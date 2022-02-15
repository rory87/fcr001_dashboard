from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView



from . import views
from .models import cable
from .models import pillar
from .models import load

urlpatterns = [
    path('analytic1', views.analytic1, name='analytic1'),
    path('analytic3', views.analytic3, name='analytic3'),
    path('analytic3data', views.analytic3_data, name='analytic3_data'),
    url(r'^data_pillars.geojson$', GeoJSONLayerView.as_view(model=pillar, properties=('network', 'feeder'), ), name='pillar_gis'),
    url(r'^data_cables.geojson$', GeoJSONLayerView.as_view(model=cable, properties=('network', 'feeder')), name='cable_gis'),
    url(r'^data_loads.geojson$', GeoJSONLayerView.as_view(model=load, properties=('network', 'feeder')), name='load_gis')
] 
