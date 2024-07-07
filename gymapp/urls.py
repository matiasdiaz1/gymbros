from django.urls import path
from django.urls import path
from .views import  admin_pedidos, agregar_al_carrito, carrito, checkout, eliminar_del_carrito, index, mis_pedidos, monedas,  personas, detallepersona, crearpersona, modificar, \
eliminar,  crear_mancuerna, lista_mancuernas, registro
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('personas/', personas, name='personas'),
    path('detallepersona/<id>', detallepersona, name='detallepersona'),
    path('crearpersona/', crearpersona, name='crearpersona'),
    path('modificar/<id>', modificar, name='modificar'),
    path('eliminar/<id>', eliminar, name='eliminar'),
    path('mancuernas/', lista_mancuernas, name='lista_mancuernas'),
    path('mancuernas/crear/', crear_mancuerna, name='crear_mancuerna'),
    path('registro/', registro, name='registro'),
    path('monedas/', monedas, name='monedas'),
    path('carrito/', carrito, name='carrito'),
    path('agregar_al_carrito/<int:mancuerna_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/<int:item_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('mis_pedidos/', mis_pedidos, name='mis_pedidos'),
    path('admin_pedidos/', admin_pedidos, name='admin_pedidos'),
    path('checkout/', checkout, name='checkout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
