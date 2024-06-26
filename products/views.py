from django.shortcuts import render,redirect,get_object_or_404
from .models import Product
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST,require_http_methods
from .forms import ProductForm
from django.contrib.auth import get_user_model
from accounts.models import User
from django.db.models import Count
# Create your views here.

def index(request):
    return render(request, 'products/index.html')

def products(request):
    if request.method=="POST":
        if request.POST.get('order')=="인기순":
            products=Product.objects.all().annotate(jjim_cnt=Count("jjim_users")).order_by("-jjim_cnt",'-created_at')
            context={"products": products}
            return render(request,"products/products.html",context)
        else:
            products=Product.objects.all().order_by('-created_at')
            context={"products": products}
            return render(request,"products/products.html",context)
    else:
        products=Product.objects.all().order_by('-created_at')
        context={"products": products}
        return render(request,"products/products.html",context)

@login_required
def product_detail(request,pk):
    product=get_object_or_404(Product,pk=pk)
    context={"product": product}
    return render(request,"products/product_detail.html",context)

@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    if request.method=="POST":
        form=ProductForm(request.POST)
        if form.is_valid():
            product=form.save(commit=False)
            product.author=request.user
            product.save()
            return redirect("products:product_detail",product.id)
    else:
        form=ProductForm()
    context={"form": form}
    return render(request,"products/create.html",context)

@login_required
@require_http_methods(["GET", "POST"])
def update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            return redirect("products:product_detail", product.pk)
    else:
        form = ProductForm(instance=product)
    context = {
        "form": form,
        "product": product,
    }
    return render(request, "products/update.html", context)

@require_POST
def delete(request,pk):
    products=get_object_or_404(Product,pk=pk)
    if request.user.is_authenticated:
        if products.author==request.user:
            products.delete()
    return redirect("products:products")

@require_POST
def jjim(request,pk):
    p=request.POST.get("pro")
    username=request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found').split('/')[-2]
    if p=="pro":
        if request.user.is_authenticated:
            product=get_object_or_404(Product,pk=pk)
            if product.jjim_users.filter(pk=request.user.id).exists():
                product.jjim_users.remove(request.user)
            else:
                product.jjim_users.add(request.user)
        else:
            return redirect("accounts:login")
        return redirect("products:products")
    elif p=='pf' or p=='s':
        if request.user.is_authenticated:
            product=get_object_or_404(Product,pk=pk)
            if product.jjim_users.filter(pk=request.user.id).exists():
                product.jjim_users.remove(request.user)
            else:
                product.jjim_users.add(request.user)
        else:
            return redirect("accounts:login")
        return redirect("accounts:profile",username)