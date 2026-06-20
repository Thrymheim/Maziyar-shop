from django.shortcuts import render, redirect, get_object_or_404
from .models import Product , Category, Newsletter, Comment
from django.contrib.auth import authenticate , login , logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import SignUpForm, SignUpFormFa
from django.http import JsonResponse
from django.db.models import Q
from .translations import TRANSLATIONS


def get_msg(request, key):
    lang = request.session.get('language', 'fa')
    msgs = {
        'fa': {
            'logged_in': 'با موفقیت وارد شدید',
            'wrong_pass': 'نام کاربری یا رمز عبور اشتباه است',
            'logged_out': '!با موفقیت خارج شدید',
            'account_created': 'اکانت شما ساخته شد!',
            'signup_error': 'مشکلی در ثبت نام شما وجود دارد!',
            'msg_sent': 'پیام شما با موفقیت ارسال شد!',
            'fill_fields': 'لطفاً تمام فیلدها را پر کنید!',
            'category_not_found': 'دسته بندی وجود ندارد',
            'username_changed': 'نام کاربری با موفقیت تغییر کرد!',
            'username_taken': 'این نام کاربری قبلاً استفاده شده است!',
            'enter_new_username': 'نام کاربری جدید را وارد کنید!',
            'password_changed': 'رمز عبور با موفقیت تغییر کرد!',
            'product_added': 'محصول با موفقیت اضافه شد!',
            'product_edited': 'محصول با موفقیت ویرایش شد!',
            'product_deleted': 'محصول با موفقیت حذف شد!',
            'category_added': 'دسته بندی با موفقیت اضافه شد!',
            'category_edited': 'دسته بندی با موفقیت ویرایش شد!',
            'category_deleted': 'دسته بندی با موفقیت حذف شد!',
            'user_activated': 'کاربر فعال شد!',
            'user_deactivated': 'کاربر غیرفعال شد!',
            'user_deleted': 'کاربر حذف شد!',
            'comment_activated': 'نظر فعال شد!',
            'comment_deactivated': 'نظر غیرفعال شد!',
            'comment_deleted': 'نظر حذف شد!',
            'enter_category_name': 'نام دسته بندی را وارد کنید!',
            'login_required': 'لطفاً ابتدا وارد شوید!',
            'no_permission': 'شما دسترسی به پنل مدیریت ندارید!',
        },
        'en': {
            'logged_in': 'Successfully logged in!',
            'wrong_pass': 'Invalid username or password',
            'logged_out': 'Successfully logged out!',
            'account_created': 'Your account has been created!',
            'signup_error': 'There was a problem with your registration!',
            'msg_sent': 'Your message has been sent successfully!',
            'fill_fields': 'Please fill in all fields!',
            'category_not_found': 'Category not found',
            'username_changed': 'Username changed successfully!',
            'username_taken': 'This username is already taken!',
            'enter_new_username': 'Please enter a new username!',
            'password_changed': 'Password changed successfully!',
            'product_added': 'Product added successfully!',
            'product_edited': 'Product edited successfully!',
            'product_deleted': 'Product deleted successfully!',
            'category_added': 'Category added successfully!',
            'category_edited': 'Category edited successfully!',
            'category_deleted': 'Category deleted successfully!',
            'user_activated': 'User activated!',
            'user_deactivated': 'User deactivated!',
            'user_deleted': 'User deleted!',
            'comment_activated': 'Comment activated!',
            'comment_deactivated': 'Comment deactivated!',
            'comment_deleted': 'Comment deleted!',
            'enter_category_name': 'Please enter a category name!',
            'login_required': 'Please login first!',
            'no_permission': 'You do not have access to the admin panel!',
        }
    }
    return msgs.get(lang, msgs['fa']).get(key, key)


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
            messages.success(request, get_msg(request, 'msg_sent'))
            return redirect('contact')
        else:
            messages.error(request, get_msg(request, 'fill_fields'))
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
             messages.success(request , get_msg(request, 'logged_in'))
             return redirect("home")
         else:
             messages.error(request , get_msg(request, 'wrong_pass'))
             return redirect("login") 

     else:    
         return render(request , 'login.html')
   

def logout_user(request):
    lang = request.session.get('language', 'fa')
    logout(request)
    request.session['language'] = lang
    messages.success(request , get_msg(request, 'logged_out'))
    return redirect("home") 


def signup_user(request):
    lang = request.session.get('language', 'fa')
    FormClass = SignUpForm if lang == 'en' else SignUpFormFa

    if request.method == "POST":
        form = FormClass(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']

            user = authenticate(request, username=username, password=password1)
            login(request, user)

            messages.success(request, get_msg(request, 'account_created'))
            return redirect("home")

        else:
            messages.error(request, get_msg(request, 'signup_error'))
            return render(request, 'signup.html', {'form': form})

    else:
        form = FormClass()
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
            return JsonResponse({'success': False, 'error': get_msg(request, 'fill_fields')}, status=400)

        if Comment.objects.filter(product=product, user=request.user).exists():
            return JsonResponse({'success': False, 'error': 'Already commented'}, status=400)

        Comment.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            body=body
        )
        return JsonResponse({'success': True, 'message': 'OK'})
    return JsonResponse({'success': False, 'error': 'Invalid'}, status=400)


@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'username':
            new_username = request.POST.get('username', '').strip()
            if new_username and new_username != request.user.username:
                if User.objects.filter(username=new_username).exists():
                    messages.error(request, get_msg(request, 'username_taken'))
                else:
                    request.user.username = new_username
                    request.user.save()
                    messages.success(request, get_msg(request, 'username_changed'))
            else:
                messages.error(request, get_msg(request, 'enter_new_username'))

        elif form_type == 'password':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, get_msg(request, 'password_changed'))
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
      messages.success(request , get_msg(request, 'category_not_found'))
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


def switch_language(request):
    lang = request.GET.get('lang', 'fa')
    if lang not in ('fa', 'en'):
        lang = 'fa'
    request.session['language'] = lang
    return redirect(request.META.get('HTTP_REFERER', '/'))


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, get_msg(request, 'login_required'))
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, get_msg(request, 'no_permission'))
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
        sale_price = request.POST.get('sale_price', '') or '0'
        product = Product(
            name=request.POST['name'],
            discription=request.POST['discription'],
            price=request.POST['price'],
            category_id=request.POST['category'],
            star=request.POST.get('star', 0),
            is_sale='is_sale' in request.POST,
            sale_price=sale_price,
        )
        if request.FILES.get('picture'):
            product.picture = request.FILES['picture']
        product.save()
        messages.success(request, get_msg(request, 'product_added'))
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
        product.sale_price = request.POST.get('sale_price', '') or '0'
        if request.FILES.get('picture'):
            product.picture = request.FILES['picture']
        product.save()
        messages.success(request, get_msg(request, 'product_edited'))
        return redirect('admin_dashboard')
    return render(request, 'admin_panel/product_form.html', {'product': product, 'categories': categories, 'editing': True})


@admin_required
def admin_product_delete(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, get_msg(request, 'product_deleted'))
        return redirect('admin_dashboard')
    return render(request, 'admin_panel/confirm_delete.html', {'item_name': f'محصول «{product.name}»'})


@admin_required
def admin_category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Category.objects.create(name=name)
            messages.success(request, get_msg(request, 'category_added'))
            return redirect('admin_dashboard')
        else:
            messages.error(request, get_msg(request, 'enter_category_name'))
    return render(request, 'admin_panel/category_form.html', {'editing': False})


@admin_required
def admin_category_edit(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            category.name = name
            category.save()
            messages.success(request, get_msg(request, 'category_edited'))
            return redirect('admin_dashboard')
        else:
            messages.error(request, get_msg(request, 'enter_category_name'))
    return render(request, 'admin_panel/category_form.html', {'category': category, 'editing': True})


@admin_required
def admin_category_delete(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, get_msg(request, 'category_deleted'))
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
        status = get_msg(request, 'user_activated') if user.is_active else get_msg(request, 'user_deactivated')
        messages.success(request, status)
    return redirect('admin_users_list')


@admin_required
def admin_user_delete(request, pk):
    user = get_object_or_404(User, id=pk)
    if user != request.user and not user.is_staff:
        user.delete()
        messages.success(request, get_msg(request, 'user_deleted'))
    return redirect('admin_users_list')


@admin_required
def admin_comments_list(request):
    return render(request, 'admin_panel/comments_list.html', {'comments': Comment.objects.select_related('user', 'product').all()})


@admin_required
def admin_comment_toggle(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    comment.is_active = not comment.is_active
    comment.save()
    status = get_msg(request, 'comment_activated') if comment.is_active else get_msg(request, 'comment_deactivated')
    messages.success(request, status)
    return redirect('admin_comments_list')


@admin_required
def admin_comment_delete(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    comment.delete()
    messages.success(request, get_msg(request, 'comment_deleted'))
    return redirect('admin_comments_list')
