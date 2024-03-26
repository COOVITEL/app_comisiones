from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Roles
from .forms import RolesForm

@login_required
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

@login_required
def deleteRole(request, id):
    rol = Roles.objects.get(id=id)
    rol.delete()
    return redirect('roles')