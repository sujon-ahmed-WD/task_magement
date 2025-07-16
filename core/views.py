from django.shortcuts import render

# Create your views here.
def home_view(request):
    return render(request, 'hom.html')

def no_permission(request):
    return render(request,'no_permission.html')