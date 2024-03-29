from django.shortcuts import render,get_object_or_404
from . models import *
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,InvalidPage

# Create your views here.
 
def home(request,c_slug=None):
    c_page=None
    prod=None
    if c_slug!=None:
        c_page=get_object_or_404(categ,slug=c_slug)
        prod=products.objects.filter(category=c_page,avilable=True)
    else:
        prod=products.objects.all().filter(avilable=True)
    cat=categ.objects.all()
    paginator=Paginator(prod,6)
    try:
        page=int(request.GET.get('page',1))
    except:
        page=1
    try:
        pro=paginator.page(page)
    except(EmptyPage,InvalidPage):
        pro=paginator.page(paginator.num_pages)
    return render(request,'home.html',{'pr':prod,'ct':cat,'pg':pro})
def prodDetails(request,c_slug,product_slug):
    try:
        prod=products.objects.get(category__slug=c_slug,slug=product_slug)
    except Exception as e:
        raise e
    
    return render(request,'item.html',{'pr':prod})



def searching(request):
    prod=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        prod=products.objects.all().filter(Q(name__contains=query)/Q(desc__contains=query))
    return render(request,'search.html',{'qr':query,'pr':prod})