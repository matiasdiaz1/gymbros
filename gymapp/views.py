
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DetallePedido, Persona, Mancuerna, CarritoItem, Pedido
from .forms import PagoForm, PedidoForm, PersonaForm, UpdatePedidoForm, UpdatePersonaForm, MancuernaForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login
import os

def es_admin(request):
    if not request.user.is_staff:
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return False
    return True

def index(request):
    mancuernas = Mancuerna.objects.all()[:6]
    return render(request, 'gymapp/index.html', {'mancuernas': mancuernas})

@login_required
def personas(request):
    people = Persona.objects.all()  
    datos = {
        "personas": people
    }
    return render(request, 'gymapp/personas.html', datos)

@login_required
def crearpersona(request):
    form = PersonaForm()
    if request.method == "POST":
        form = PersonaForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'La persona ha sido agregada exitosamente.')
            return redirect(to="personas")
    datos = {
        "form": form
    }
    return render(request, 'gymapp/crearpersona.html', datos)

@login_required
def detallepersona(request, id):
    persona = get_object_or_404(Persona, rut=id)
    mancuernas = Mancuerna.objects.all()
    datos = {
        "persona": persona,
        "mancuernas": mancuernas
    }
    return render(request, 'gymapp/detallepersona.html', datos)

@login_required
def modificar(request, id):
    persona = get_object_or_404(Persona, rut=id)
    form = UpdatePersonaForm(instance=persona)
    if request.method == "POST":
        form = UpdatePersonaForm(data=request.POST, files=request.FILES, instance=persona)
        if form.is_valid():
            form.save()
            messages.warning(request, 'La persona ha sido modificada exitosamente.')
            return redirect(to="personas")
    datos = {
        "form": form,
        "persona": persona
    }
    return render(request, 'gymapp/modificar.html', datos)

@login_required
def eliminar(request, id):
    persona = get_object_or_404(Persona, rut=id)
    if request.method == "POST":
        if persona.foto:
            if os.path.isfile(persona.foto.path):
                os.remove(persona.foto.path)
        persona.delete()
        messages.error(request, 'La persona ha sido eliminada exitosamente.')
        return redirect(to="personas")
    datos = {
        "persona": persona
    }
    return render(request, 'gymapp/eliminar.html', datos)


@login_required
def modificar_mancuerna(request, id):
    mancuerna = get_object_or_404(Mancuerna, id=id)
    if request.method == 'POST':
        form = MancuernaForm(request.POST, instance=mancuerna)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mancuerna modificada exitosamente.')
            return redirect('lista_mancuernas')
    else:
        form = MancuernaForm(instance=mancuerna)
    return render(request, 'gymapp/modificar_mancuerna.html', {'form': form})

@login_required
def eliminar_mancuerna(request, id):
    mancuerna = get_object_or_404(Mancuerna, id=id)
    if request.method == 'POST':
        mancuerna.delete()
        messages.success(request, 'Mancuerna eliminada exitosamente.')
        return redirect('lista_mancuernas')
    return render(request, 'gymapp/eliminar_mancuerna.html', {'mancuerna': mancuerna})

@login_required
def lista_mancuernas(request):
    mancuernas = Mancuerna.objects.all()
    return render(request, 'gymapp/lista_mancuernas.html', {'mancuernas': mancuernas})

@login_required
def crear_mancuerna(request):
    if request.method == 'POST':
        form = MancuernaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_mancuernas')
    else:
        form = MancuernaForm()
    return render(request, 'gymapp/crear_mancuerna.html', {'form': form})

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    
    if request.method == "POST":
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            return redirect(to="index")
        data["form"] = formulario
    
    return render(request, 'registration/registro.html', data)

@login_required
def monedas(request):
    return render(request, 'gymapp/monedas.html')

@login_required
def carrito(request):
    carrito_items = CarritoItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in carrito_items)
    return render(request, 'gymapp/carrito.html', {'carrito_items': carrito_items, 'total': total})

@login_required
def agregar_al_carrito(request, mancuerna_id):
    mancuerna = get_object_or_404(Mancuerna, id=mancuerna_id)
    carrito_item, created = CarritoItem.objects.get_or_create(user=request.user, mancuerna=mancuerna)
    if not created:
        if carrito_item.quantity < mancuerna.stock:
            carrito_item.quantity += 1
            carrito_item.save()
        else:
            messages.error(request, 'No hay suficiente stock disponible.')
    else:
        carrito_item.quantity = 1
        carrito_item.save()
    messages.success(request, 'Mancuerna agregada al carrito.')
    return redirect('carrito')

@login_required
def eliminar_del_carrito(request, item_id):
    carrito_item = get_object_or_404(CarritoItem, id=item_id, user=request.user)
    carrito_item.delete()
    messages.success(request, 'Mancuerna eliminada del carrito.')
    return redirect('carrito')

@login_required
def actualizar_carrito(request, item_id):
    carrito_item = get_object_or_404(CarritoItem, id=item_id, user=request.user)
    if request.method == 'POST':
        nueva_cantidad = int(request.POST.get('cantidad'))
        if nueva_cantidad <= carrito_item.mancuerna.stock:
            carrito_item.quantity = nueva_cantidad
            carrito_item.save()
            messages.success(request, 'Cantidad actualizada exitosamente.')
        else:
            messages.error(request, 'No hay suficiente stock disponible.')
    return redirect('carrito')

@login_required
def checkout(request):
    carrito_items = CarritoItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in carrito_items)
    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)
        pago_form = PagoForm(request.POST)
        if pedido_form.is_valid() and pago_form.is_valid():
            pedido = pedido_form.save(commit=False)
            pedido.user = request.user
            pedido.total = total
            pedido.save()
            for item in carrito_items:
                DetallePedido.objects.create(
                    pedido=pedido,
                    mancuerna=item.mancuerna,
                    cantidad=item.quantity,
                    precio_unitario=item.mancuerna.precio
                )
                # Disminuir el stock de la mancuerna
                item.mancuerna.stock -= item.quantity
                item.mancuerna.save()
            carrito_items.delete()
            messages.success(request, 'Pedido realizado con éxito.')
            return redirect('mis_pedidos')
    else:
        pedido_form = PedidoForm()
        pago_form = PagoForm()
    return render(request, 'gymapp/checkout.html', {'carrito_items': carrito_items, 'total': total, 'pedido_form': pedido_form, 'pago_form': pago_form})

@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(user=request.user)
    detalles_pedidos = DetallePedido.objects.filter(pedido__in=pedidos)
    return render(request, 'gymapp/mis_pedidos.html', {'pedidos': pedidos, 'detalles_pedidos': detalles_pedidos})

@login_required
def admin_pedidos(request):
    if not request.user.is_staff:
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('index')
    
    if request.method == 'POST':
        if 'update' in request.POST:
            pedido_id = request.POST.get('pedido_id')
            pedido = get_object_or_404(Pedido, id=pedido_id)
            form = UpdatePedidoForm(request.POST, instance=pedido)
            if form.is_valid():
                form.save()
                messages.success(request, 'Estado del pedido actualizado con éxito.')
        elif 'delete' in request.POST:
            pedido_id = request.POST.get('pedido_id')
            pedido = get_object_or_404(Pedido, id=pedido_id)
            pedido.delete()
            messages.success(request, 'Pedido eliminado con éxito.')
    
    pedidos = Pedido.objects.all()
    detalles_pedidos = DetallePedido.objects.all()
    return render(request, 'gymapp/admin_pedidos.html', {'pedidos': pedidos, 'detalles_pedidos': detalles_pedidos, 'form': UpdatePedidoForm()})

