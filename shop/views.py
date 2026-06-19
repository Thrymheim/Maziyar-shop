from django.shortcuts import render, redirect, get_object_or_404
from .models import Product , Category, Newsletter, Comment
from django.contrib.auth import authenticate , login , logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import SignUpForm
from django.http import JsonResponse
from django.db.models import Q


def helloworld(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    filters = {}

    category = request.GET.get('category', '')
    if category:
        products = products.filter(category__name=category)
        filters['category'] = category

    price_min = request.GET.get('price_min', '')
    if price_min:
        products = products.filter(price__gte=price_min)
        filters['price_min'] = price_min

    price_max = request.GET.get('price_max', '')
    if price_max:
        products = products.filter(price__lte=price_max)
        filters['price_max'] = price_max

    rating = request.GET.get('rating', '')
    if rating:
        products = products.filter(star__gte=int(rating))
        filters['rating'] = rating

    sort = request.GET.get('sort', '')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-star')
    elif sort == 'newest':
        products = products.order_by('-id')
    elif sort == 'sale':
        products = products.filter(is_sale=True)
    if sort:
        filters['sort'] = sort

    return render(request, 'index.html', {'products': products, 'categories': categories, 'filters': filters})

def about(request):
    return render(request , 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        if name and email and message:
            messages.success(request, 'پیام شما با موفقیت ارسال شد!')
            return redirect('contact')
        else:
            messages.error(request, 'لطفاً تمام فیلدها را پر کنید!')
    return render(request, 'contact.html')

def terms(request):
    return render(request , 'terms.html')

def login_user(request):
     if request.method == "POST":  
         username = request.POST.get('username', '') 
         password = request.POST.get('password', '')

         user = authenticate(request , username= username , password=password)
         if user is not None:
             login(request , user)
             messages.success(request , ("با موفقیت وارد شدید"))
             return redirect("home")
         else:
             messages.error(request , ("نام کاربری یا رمز عبور اشتباه است"))
             return redirect("login") 

     else:    
         return render(request , 'login.html')
   

def logout_user(request):
    logout(request)
    messages.success(request , ("!با موفقیت خارج شدید"))
    return redirect("home") 


def signup_user(request):
    
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']

            user = authenticate(request, username=username, password=password1)
            login(request, user)

            messages.success(request, 'اکانت شما ساخته شد!')
            return redirect("home")

        else:
            messages.error(request, 'مشکلی در ثبت نام شما وجود دارد!')
            return render(request, 'signup.html', {'form': form})

    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})



def product(request, pk): 
    product = get_object_or_404(Product, id=pk)
    comments = product.comment_set.filter(is_active=True)
    return render(request , 'product.html' , {'product' : product, 'comments': comments})


@login_required(login_url='login')
def add_comment(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=pk)
        rating = int(request.POST.get('rating', 5))
        body = request.POST.get('body', '').strip()

        if not body:
            return JsonResponse({'success': False, 'error': 'متن نظر را وارد کنید'}, status=400)

        if Comment.objects.filter(product=product, user=request.user).exists():
            return JsonResponse({'success': False, 'error': 'شما قبلاً برای این محصول نظر ثبت کرده‌اید'}, status=400)

        Comment.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            body=body
        )
        return JsonResponse({'success': True, 'message': 'نظر شما با موفقیت ثبت شد!'})
    return JsonResponse({'success': False, 'error': 'درخواست نامعتبر'}, status=400)


@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'username':
            new_username = request.POST.get('username', '').strip()
            if new_username and new_username != request.user.username:
                if User.objects.filter(username=new_username).exists():
                    messages.error(request, 'این نام کاربری قبلاً استفاده شده است!')
                else:
                    request.user.username = new_username
                    request.user.save()
                    messages.success(request, 'نام کاربری با موفقیت تغییر کرد!')
            else:
                messages.error(request, 'نام کاربری جدید را وارد کنید!')

        elif form_type == 'password':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'رمز عبور با موفقیت تغییر کرد!')
            else:
                for error in form.errors.values():
                    messages.error(request, error.as_text())

        return redirect('profile')

    return render(request, 'profile.html')


def search(request):
    query = request.GET.get('q', '').strip()
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(discription__icontains=query)
        )
    else:
        products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'index.html', {'products': products, 'categories': categories, 'query': query, 'filters': {}})


def category(request,cat):
    cat = cat.replace("-"," ")
    try:
      category = Category.objects.get(name = cat)
      products = Product.objects.filter(category = category)
      return render(request , 'category.html' , {'products' : products , "category": category})
    except:
      messages.success(request , ('دسته بندی وجود ندارد'))
      return redirect("home")


def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if not email:
            return JsonResponse({'success': False, 'error': 'ایمیل را وارد کنید'}, status=400)
        obj, created = Newsletter.objects.get_or_create(email=email)
        if not created and not obj.is_active:
            obj.is_active = True
            obj.save()
        return JsonResponse({'success': True, 'message': 'با موفقیت در خبرنامه عضو شدید!'})
    return JsonResponse({'success': False, 'error': 'درخواست نامعتبر'}, status=400)


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'لطفاً ابتدا وارد شوید!')
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, 'شما دسترسی به پنل مدیریت ندارید!')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    context = {
        'products': Product.objects.all(),
        'categories': Category.objects.all(),
        'stats': {
            'products': Product.objects.count(),
            'categories': Category.objects.count(),
            'users': User.objects.count(),
            'comments': Comment.objects.count(),
        },
        'recent_comments': Comment.objects.select_related('user', 'product')[:5],
    }
    return render(request, 'admin_panel/dashboard.html', context)


@admin_required
def admin_product_add(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        product = Product(
            name=request.POST['name'],
            discription=request.POST['discription'],
            price=request.POST['price'],
            category_id=request.POST['category'],
            star=request.POST.get('star', 0),
            is_sale='is_sale' in request.POST,
            sale_price=request.POST.get('sale_price', 0),
        )
        if request.FILES.get('picture'):
            product.picture = request.FILES['picture']
        product.save()
        messages.success(request, 'محصول با موفقیت اضافه شد!')
        return redirect('admin_dashboard')
    return render(request, 'admin_panel/product_form.html', {'categories': categories, 'editing': False})


@admin_required
def admin_product_edit(request, pk):
    product = get_object_or_404(Product, id=pk)
    categories = Category.objects.all()
    if request.method == 'POST':
        product.name = request.POST['name']
        product.discription = request.POST['discription']
        product.price = request.POST['price']
        product.category_id = request.POST['category']
        product.star = request.POST.get('star', 0)
        product.is_sale = 'is_sale' in request.POST
        product.sale_price = request.POST.get('sale_price', 0)
        if request.FILES.get('picture'):
            product.picture = request.FILES['picture']
        product.save()
        messages.success(request, 'محصول با موفقیت ویرایش شد!')
        return redirect('admin_dashboard')
    return render(request, 'admin_panel/product_form.html', {'product': product, 'categories': categories, 'editing': True})


@admin_required
def admin_product_delete(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'محصول با موفقیت حذف شد!')
        return redirect('admin_dashboard')
    return render(request, 'admin_panel/confirm_delete.html', {'item_name': f'محصول «{product.name}»'})


@admin_required
def admin_category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Category.objects.create(name=name)
            messages.success(request, 'دسته بندی با موفقیت اضافه شد!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'نام دسته بندی را وارد کنید!')
    return render(request, 'admin_panel/category_form.html', {'editing': False})


@admin_required
def admin_category_edit(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            category.name = name
            category.save()
            messages.success(request, 'دسته بندی با موفقیت ویرایش شد!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'نام دسته بندی را وارد کنید!')
    return render(request, 'admin_panel/category_form.html', {'category': category, 'editing': True})


@admin_required
def admin_category_delete(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'دسته بندی با موفقیت حذف شد!')
        return redirect('admin_dashboard')
    return render(request, 'admin_panel/confirm_delete.html', {'item_name': f'دسته بندی «{category.name}»'})


@admin_required
def admin_products_list(request):
    products = Product.objects.all()
    all_categories = Category.objects.all()
    filters = {}

    q = request.GET.get('q', '').strip()
    if q:
        products = products.filter(name__icontains=q)
        filters['q'] = q

    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)
        filters['category'] = category_id

    price_min = request.GET.get('price_min', '')
    if price_min:
        products = products.filter(price__gte=price_min)
        filters['price_min'] = price_min

    price_max = request.GET.get('price_max', '')
    if price_max:
        products = products.filter(price__lte=price_max)
        filters['price_max'] = price_max

    rating = request.GET.get('rating', '')
    if rating:
        products = products.filter(star__gte=int(rating))
        filters['rating'] = rating

    sort = request.GET.get('sort', '')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'rating_desc':
        products = products.order_by('-star')
    elif sort == 'newest':
        products = products.order_by('-id')
    elif sort == 'sale':
        products = products.filter(is_sale=True)
    if sort:
        filters['sort'] = sort

    return render(request, 'admin_panel/products_list.html', {
        'products': products,
        'all_categories': all_categories,
        'filters': filters,
    })


@admin_required
def admin_categories_list(request):
    return render(request, 'admin_panel/categories_list.html', {'categories': Category.objects.all()})


@admin_required
def admin_users_list(request):
    return render(request, 'admin_panel/users_list.html', {'users': User.objects.all().order_by('-date_joined')})


@admin_required
def admin_user_toggle(request, pk):
    user = get_object_or_404(User, id=pk)
    if user != request.user and not user.is_staff:
        user.is_active = not user.is_active
        user.save()
        status = 'فعال' if user.is_active else 'غیرفعال'
        messages.success(request, f'کاربر «{user.username}» {status} شد!')
    return redirect('admin_users_list')


@admin_required
def admin_user_delete(request, pk):
    user = get_object_or_404(User, id=pk)
    if user != request.user and not user.is_staff:
        user.delete()
        messages.success(request, f'کاربر «{user.username}» حذف شد!')
    return redirect('admin_users_list')


@admin_required
def admin_comments_list(request):
    return render(request, 'admin_panel/comments_list.html', {'comments': Comment.objects.select_related('user', 'product').all()})


@admin_required
def admin_comment_toggle(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    comment.is_active = not comment.is_active
    comment.save()
    status = 'فعال' if comment.is_active else 'غیرفعال'
    messages.success(request, f'نظر «{comment.user.username}» {status} شد!')
    return redirect('admin_comments_list')


@admin_required
def admin_comment_delete(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    comment.delete()
    messages.success(request, 'نظر با موفقیت حذف شد!')
    return redirect('admin_comments_list')
