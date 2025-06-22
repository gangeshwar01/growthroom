from django.shortcuts import render, redirect, get_object_or_404
from .models import CertificateRequest
from .forms import CertificateRequestForm

# Create your views here.

def certificates_home(request):
    return render(request, 'certificates/home.html')

def certificate_list(request):
    certificates = CertificateRequest.objects.all()
    return render(request, 'certificates/certificate_list.html', {'certificates': certificates})

def certificate_detail(request, pk):
    certificate = get_object_or_404(CertificateRequest, pk=pk)
    return render(request, 'certificates/certificate_detail.html', {'certificate': certificate})

def certificate_create(request):
    if request.method == 'POST':
        form = CertificateRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('certificate_list')
    else:
        form = CertificateRequestForm()
    return render(request, 'certificates/certificate_form.html', {'form': form})

def certificate_update(request, pk):
    certificate = get_object_or_404(CertificateRequest, pk=pk)
    if request.method == 'POST':
        form = CertificateRequestForm(request.POST, instance=certificate)
        if form.is_valid():
            form.save()
            return redirect('certificate_list')
    else:
        form = CertificateRequestForm(instance=certificate)
    return render(request, 'certificates/certificate_form.html', {'form': form})

def certificate_delete(request, pk):
    certificate = get_object_or_404(CertificateRequest, pk=pk)
    if request.method == 'POST':
        certificate.delete()
        return redirect('certificate_list')
    return render(request, 'certificates/certificate_confirm_delete.html', {'certificate': certificate})
