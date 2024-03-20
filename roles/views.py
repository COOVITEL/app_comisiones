from django.shortcuts import render, redirect
from .models import Roles
from .forms import RolesForm

def roles(request):
    roles = Roles.objects.all()
    form = RolesForm()
    if request.method == "POST":
        form = RolesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('roles')
    return render(request, 'roles.html', {
                    'roles': roles,
                    'form': form})

def deleteRole(request, id):
    rol = Roles.objects.get(id=id)
    rol.delete()
    return redirect('roles')