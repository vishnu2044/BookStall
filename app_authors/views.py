from django.shortcuts import render

# Create your views here.
def admin_authors(request):
    return render(request, 'adminpanel/authors.html' )

def add_author(request):
    return render(request, 'adminpanel/add_author.html')