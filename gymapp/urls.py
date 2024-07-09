from django.urls import path
from django.urls import path
from .views import  actualizar_carrito, admin_pedidos, agregar_al_carrito, carrito, checkout, eliminar_del_carrito, eliminar_mancuerna, get_comunas, index, mis_pedidos, modificar_mancuerna, monedas,  personas, detallepersona, crearpersona, modificar, \
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
    path('mancuernas/modificar/<int:id>/', modificar_mancuerna, name='modificar_mancuerna'),
    path('mancuernas/eliminar/<int:id>/', eliminar_mancuerna, name='eliminar_mancuerna'),
    path('registro/', registro, name='registro'),
    path('monedas/', monedas, name='monedas'),
    path('carrito/', carrito, name='carrito'),
    path('carrito/agregar/<int:mancuerna_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:item_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/actualizar/<int:item_id>/', actualizar_carrito, name='actualizar_carrito'),
    path('mis_pedidos/', mis_pedidos, name='mis_pedidos'),
    path('admin_pedidos/', admin_pedidos, name='admin_pedidos'),
    path('checkout/', checkout, name='checkout'),
    path('get-comunas/', get_comunas, name='get_comunas'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
