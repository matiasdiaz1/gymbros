from django.contrib import admin
from .models import Persona, Mancuerna, CarritoItem, Pedido, DetallePedido

class PersonaAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'apellido', 'fnacto', 'correo', 'sexo')
    search_fields = ('rut', 'nombre', 'apellido', 'correo')
    list_filter = ('sexo',)

class MancuernaAdmin(admin.ModelAdmin):
    list_display = ('peso', 'precio', 'stock')
    search_fields = ('peso', 'precio')
    list_filter = ('peso', 'precio')

class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'mancuerna', 'quantity', 'created_at')
    search_fields = ('user__username', 'mancuerna__peso')
    list_filter = ('created_at',)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('user', 'total', 'created_at', 'estado', 'region', 'comuna', 'calle', 'numero', 'dpto_casa_oficina')
    search_fields = ('user__username', 'estado', 'region', 'comuna', 'calle', 'numero')
    list_filter = ('estado', 'created_at', 'region', 'comuna')

class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'mancuerna', 'cantidad', 'precio_unitario')
    search_fields = ('pedido__id', 'mancuerna__peso')
    list_filter = ('pedido',)
admin.site.register(Persona, PersonaAdmin)
admin.site.register(Mancuerna, MancuernaAdmin)
admin.site.register(CarritoItem, CarritoItemAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(DetallePedido, DetallePedidoAdmin)