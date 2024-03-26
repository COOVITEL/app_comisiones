from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Asesor, Sucursale, File
from .forms import FileForm, AsesorForm

@login_required
def asesores(request):
    """"""
    permission = False
    if request.user.is_superuser:
        permission = True
    citys = Sucursale.objects.all()
    
    form = AsesorForm()
    if request.method == 'POST':
        form = AsesorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asesores')

    city = request.GET.get("ciudad", None)
    todos = request.GET.get("todos", None)
    
    if todos is not None:
        asesores = Asesor.objects.all().order_by('id')
    elif city is None or city == "":
        asesores = Asesor.objects.all().order_by('id')
    else:
        asesores = Asesor.objects.filter(sucursal__city=city).order_by('id')

    paginator = Paginator(asesores, 5)
    page_number = request.GET.get('page', 1)

    try:
        asesors = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        asesors = paginator.page(1)
    
    return render(request, "users/asesores.html", {"asesors": asesors,
                                                   "form": form,
                                                   "permission": permission,
                                                   "citys": citys})
    
@login_required
def deleteasesor(request, id):
    """"""
    asesor = Asesor.objects.get(id=id)
    asesor.delete()
    return redirect('asesores')

@login_required
def sucursales(request):
    """"""
    user_permissions = False
    if request.user.is_superuser:
        user_permissions = True
    citys = Sucursale.objects.all()
    if request.method == "POST":
        city = request.POST['city']
        create = Sucursale(city=city)
        create.save()
        return redirect("sucursales")
    return render(request, "users/sucursales.html",
                            {"citys": citys,
                             "permission": user_permissions})

@login_required
def deleteSucursal(request, id):
    """"""
    sucursal = Sucursale.objects.get(id=id)
    sucursal.delete()
    return redirect("sucursales")

@login_required
def files(request):
    files = File.objects.all().order_by('-year', '-month')
    paginator = Paginator(files, 5)
    page_number = request.GET.get('page')
    
    try:
        files = paginator.page(page_number)
    except PageNotAnInteger:
        files = paginator.page(1)
    except EmptyPage:
        files = paginator.page(paginator.num_pages)
    
    form = FileForm()
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('files')
        
    return render(request, 'users/files.html', {'files': files, 'form': form})

@login_required
def optionsFiles(request):
    """"""
    files = File.objects.all().order_by('-year', '-month')
    paginator = Paginator(files, 6)
    page_number = request.GET.get('page', 1)
    try:
        list_files = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        list_files = paginator.page(1)
    
    return render(request, 'users/list_files.html',
                  {'files': list_files})
    
@login_required
def optionsAsesors(request, file):
    """"""
    asesors = Asesor.objects.all()
    request.session['file'] = file
    
    return render(request, 'users/list_asesors.html',
                  {'asesors': asesors, 'file': file})   