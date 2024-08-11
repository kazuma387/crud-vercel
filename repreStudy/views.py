from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Representante, Alumno, RegistroEliminado
from .forms import RepresentanteForm, AlumnoForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
import json


# para el login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # lógica de autenticación
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                # Lógica después de autenticar correctamente
                return redirect('index')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def home(request):
    return render(request, './index.html')

##############################################################################################################################################

@login_required
def representante_index(request, letter = None):
    # para buscar por la primera letra
    if letter != None:
        search_query = None
        representantes = Representante.objects.filter(nombres__istartswith=letter)
    else:
        # para el buscador
        search_query = request.GET.get('search', '')
        representantes = Representante.objects.filter(
            Q(nombres__icontains=search_query) |
            Q(apellidos__icontains=search_query) |
            Q(cedula__contains=search_query) |
            Q(serial_patria__contains=search_query) |
            Q(codigo_patria__contains=search_query)
        )

    # Verificar si no se encontraron representantes
    no_results_message = "No se encontraron coincidencias." if not representantes.exists() else None

    # Paginación
    paginator = Paginator(representantes, 7)  # Mostrar 7 representantes por página
    page_number = request.GET.get('page')  # Obtener el número de página de la solicitud
    try:
        page_obj = paginator.get_page(page_number)  # Obtener la página solicitada
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)  # Si no es un número entero, mostrar la primera página
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)  # Si está fuera del rango, mostrar la última página

    context = {
        'representantes': page_obj,  # Usar el objeto de la página en lugar de la lista completa
        'no_results_message': no_results_message,
        'search_query': search_query  # Pasar la consulta de búsqueda al contexto si existe
    }
    return render(request, 'representante/index.html', context)


# ver info representante
@login_required
def representante_view(request, id):
    representante = Representante.objects.get(id=id)
    alumnos = Alumno.objects.filter(representante=representante)
    context = {
        'representante': representante,
        'alumnos': alumnos
    }
    return render(request, 'representante/detail.html', context)


# para editar representante
@permission_required('repreStudy.change_representante')
@login_required
def representante_edit(request, id):
    representante = Representante.objects.get(id=id)

    # para que al darle al boton de editar nos muestre el formulario lleno y poder editarlo
    if request.method == 'GET':
        form = RepresentanteForm(instance=representante)
        context = {
            'form' : form,
            'id' : id
        }
        return render(request, 'representante/edit.html', context)

    # para que al editarlo y darle a guardar este guarde lo editado y sustituya al anterior
    if request.method == 'POST':
        form = RepresentanteForm(request.POST, instance=representante)
        if form.is_valid():
            form.save()
        context = {
            'form' : form,
            'id' : id
        }
        messages.success(request, "Representante actualizado.")
        return render(request, 'representante/edit.html', context)


# para añadir un representante nuevo
@permission_required('repreStudy.add_representante')
@login_required
def representante_create(request):
    # para darle al boton añadir y crear el formulario
    if request.method == 'GET':
        form = RepresentanteForm()
        context = {
            'form' : form
        }
        return render(request, 'representante/create.html', context)
    
    # para crear y guardar el nuevo contacto
    if request.method == 'POST':
        form = RepresentanteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Representante registrado exitosamente.")
            return redirect('representante_create')
    else:
        form = RepresentanteForm()
    
    context = {
        'form': form
    }
    return render(request, 'representante/create.html', context)
        
    

# para eliminar un representante
@permission_required('repreStudy.delete_representante')
@login_required
def representante_delete(request, id):
    return redirect('representante_confirm_delete', id=id)    


# para confirmar si desea eliminarlo
@permission_required('repreStudy.delete_representante')
@login_required
def representante_confirm_delete(request, id):
    representante = get_object_or_404(Representante, id=id)
    if request.method == 'POST':
        # para que si hay un error en el registro no se guarde nada 
        with transaction.atomic():
            # Guardar el registro del representante eliminado
            datos_representante = {
                'id': representante.id,
                'nombres': representante.nombres,
                'apellidos': representante.apellidos,
                'cedula': representante.cedula,
                # Añade aquí todos los campos relevantes del representante
            }
            RegistroEliminado.objects.create(
                tipo='representante',
                datos=datos_representante,
                eliminado_por=request.user
            )
            
            # Guardar los registros de los alumnos asociados
            alumnos = Alumno.objects.filter(representante=representante)
            for alumno in alumnos:
                datos_alumno = {
                    'id': alumno.id,
                    'nombres': alumno.nombres,
                    'apellidos': alumno.apellidos,
                    'edad': alumno.edad,
                    'sexo': alumno.sexo,
                    'grado_y_seccion': alumno.grado_y_seccion,
                    'representante_cedula': alumno.representante.cedula if alumno.representante else None,
                    # Añade aquí todos los campos relevantes del alumno
                }
                RegistroEliminado.objects.create(
                    tipo='alumno',
                    datos=datos_alumno,
                    eliminado_por=request.user
                )
            
            # Eliminar el representante (esto eliminará automáticamente los alumnos asociados)
            representante.delete()
        
        messages.success(request, "Representante y sus alumnos asociados eliminados")
        return redirect('representante')
    context = {
        'representante': representante
    }
    return render(request, 'representante/representante_confirm_delete.html', context)


################################################################################################

@login_required
def alumno_index(request, letter=None):
    if letter is not None:
        search_query = None
        alumnos = Alumno.objects.filter(nombres__istartswith=letter)
    else:
        search_query = request.GET.get('search', '')
        alumnos = Alumno.objects.filter(
            Q(nombres__icontains=search_query) |
            Q(apellidos__icontains=search_query) |
            Q(grado_y_seccion__icontains=search_query) |
            Q(sexo__icontains=search_query) |
            Q(edad__icontains=search_query)
        )

    no_results_message = "No se encontraron coincidencias." if not alumnos.exists() else None

    paginator = Paginator(alumnos, 8)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'alumnos': page_obj,
        'no_results_message': no_results_message,
        'search_query': search_query
    }
    return render(request, 'alumno/index.html', context)


@login_required
def alumno_view(request, id):
    alumno = Alumno.objects.get(id=id)
    context = {
        'alumno': alumno
    }
    return render(request, 'alumno/detail.html', context)


@permission_required('repreStudy.change_alumno')
@login_required
def alumno_edit(request, id):
    alumno = Alumno.objects.get(id=id)

    if request.method == 'GET':
        form = AlumnoForm(instance=alumno)
        context = {
            'form': form,
            'id': id
        }
        return render(request, 'alumno/edit.html', context)

    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
        context = {
            'form': form,
            'id': id
        }
        messages.success(request, "alumno actualizado.")
        return render(request, 'alumno/edit.html', context)


@permission_required('repreStudy.add_alumno')
@login_required
def alumno_create(request):
    if request.method == 'GET':
        form = AlumnoForm()
        context = {
            'form': form
        }
        return render(request, 'alumno/create.html', context)

    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
        messages.success(request, "alumno añadido.")
        return redirect('alumno_create')


@permission_required('repreStudy.delete_alumno')
@login_required
def alumno_delete(request, id):
    return redirect('alumno_confirm_delete', id=id)


@permission_required('repreStudy.delete_alumno')
@login_required
def alumno_confirm_delete(request, id):
    alumno = get_object_or_404(Alumno, id=id)
    if request.method == 'POST':
        # Guardar el registro eliminado
        datos = {
            'id': alumno.id,
            'nombres': alumno.nombres,
            'apellidos': alumno.apellidos,
            'edad': alumno.edad,
            'sexo': alumno.sexo,
            'grado_y_seccion': alumno.grado_y_seccion,
            'representante_cedula': alumno.representante.cedula if alumno.representante else None,
            # Añade aquí todos los campos relevantes
        }
        RegistroEliminado.objects.create(
            tipo='alumno',
            datos=datos,
            eliminado_por=request.user
        )
        
        alumno.delete()
        messages.success(request, "Alumno eliminado")
        return redirect('alumno')
    context = {
        'alumno': alumno
    }
    return render(request, 'alumno/alumno_confirm_delete.html', context)
