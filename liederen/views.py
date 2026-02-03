from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse, Http404


from .models import Lied
from .forms import LiedForm


@login_required
def liedlijst(request):
    liederen = Lied.objects.filter(actief=True)
    return render(request, 'liedlijst.html', {'liederen': liederen})


@login_required
def lied_pdf(request, pk):
    lied = get_object_or_404(Lied, pk=pk, actief=True)

    if not lied.pdf.storage.exists(lied.pdf.name):
        raise Http404

    return FileResponse(
        lied.pdf.open('rb'),
        content_type='application/pdf'
    )


@staff_member_required
def lied_manage_list(request):
    liederen = Lied.objects.all()
    return render(request, 'lied_manage_list.html', {'liederen': liederen})


@staff_member_required
def lied_create(request):
    if request.method == 'POST':
        form = LiedForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lied toegevoegd.')
            return redirect('liederen:lied_manage_list')
    else:
        form = LiedForm()

    return render(request, 'lied_form.html', {'form': form, 'mode': 'create'})


@staff_member_required
def lied_edit(request, pk):
    lied = get_object_or_404(Lied, pk=pk)

    if request.method == 'POST':
        form = LiedForm(request.POST, request.FILES, instance=lied)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lied opgeslagen.')
            return redirect('liederen:lied_manage_list')
    else:
        form = LiedForm(instance=lied)

    return render(
        request,
        'lied_form.html',
        {'form': form, 'mode': 'edit', 'lied': lied}
    )


@staff_member_required
def lied_delete(request, pk):
    lied = get_object_or_404(Lied, pk=pk)

    if request.method == 'POST':
        lied.delete()
        messages.success(request, 'Lied verwijderd.')
        return redirect('liederen:lied_manage_list')

    return render(request, 'lied_confirm_delete.html', {'lied': lied})
