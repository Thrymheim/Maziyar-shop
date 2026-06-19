# مازیار شاپ | Maziyar Shop

فروشگاه آنلاین مازیار شاپ — یک پروژه کامل فروشگاه اینترنتی ساخته شده با Django

## نمای کلی

مازیار شاپ یک فروشگاه آنلاین با امکانات کامل شامل مدیریت محصولات، سبد خرید، سیستم نظر و امتیاز، خبرنامه، پنل مدیریت، و تم تاریک/روشن است.

## امکانات

### کاربران
- ثبت نام و ورود
- تغییر نام کاربری و رمز عبور
- پروفایل کاربری
- امتیاز و نظردهی به محصولات (فقط کاربران وارد شده)

### محصولات
- نمایش محصولات با تصویر، قیمت، امتیاز و توضیحات
- فیلتر بر اساس دسته بندی، قیمت، امتیاز و مرتب سازی
- جستجوی محصولات
- نمایش تخفیف‌ها

### سبد خرید
- افزودن به سبد خرید (AJAX)
- تغییر تعداد محصولات
- حذف محصول از سبد

### پنل مدیریت
- داشبورد با آمار کلی (محصولات، دسته بندی‌ها، کاربران، نظرات)
- مدیریت محصولات (افزودن، ویرایش، حذف)
- مدیریت دسته بندی‌ها
- مدیریت کاربران (فعال/غیرفعال کردن، حذف)
- مدیریت نظرات (نمایش/پنهان کردن، حذف)
- فیلتر پیشرفته محصولات در پنل مدیریت

### طراحی
- ریسپانسیو (سازگار با موبایل و دسکتاپ)
- تم تاریک و روشن
- فونت وزیرمتن فارسی
- آیکون‌های Bootstrap Icons
- فریم‌ورک Bootstrap 5

## تکنولوژی‌ها

| بخش | تکنولوژی |
|------|----------|
| Backend | Django 5.0 |
| Database | SQLite (توسعه) / PostgreSQL (تولید) |
| Frontend | Bootstrap 5, jQuery |
| فونت | Vazirmatn |
| آیکون | Bootstrap Icons |
| استاتیک فایل | WhiteNoise |
| سرور | Gunicorn |

## نصب و راه اندازی

### پیش نیازها
- Python 3.11+
- pip

### مراحل نصب

```bash
# کلون کردن پروژه
git clone https://github.com/Thrymheim/Maziyar-shop.git
cd Maziyar-shop

# ساخت محیط مجازی
python -m venv venv
source venv/bin/activate  # لینوکس/مک
venv\Scripts\activate     # ویندوز

# نصب وابستگی‌ها
pip install -r requirements.txt

# اجرای مایگریشن‌ها
python manage.py migrate

# ساخت ادمین
python manage.py createsuperuser

# اجرای سرور
python manage.py runserver
```

سایت در آدرس `http://127.0.0.1:8000` قابل دسترسی است.

## ساختار پروژه

```
Maziyar-shop/
├── digikala/              # تنظیمات پروژه
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── shop/                  # اپلیکیشن اصلی فروشگاه
│   ├── models.py          # مدل‌ها (Product, Category, Comment, Newsletter)
│   ├── views.py           # ویوها
│   ├── urls.py            # مسیرها
│   ├── forms.py           # فرم‌ها
│   ├── admin.py           # ادمین جنگو
│   └── templates/         # قالب‌ها
│       ├── base.html
│       ├── navbar.html
│       ├── index.html
│       ├── product.html
│       ├── profile.html
│       ├── contact.html
│       └── admin_panel/   # قالب‌های پنل مدیریت
├── cart/                  # اپلیکیشن سبد خرید
│   ├── cart.py
│   ├── views.py
│   └── context_processors.py
├── static/                # فایل‌های استاتیک
│   ├── css/
│   ├── js/
│   ├── fonts/
│   └── assets/
├── media/                 # فایل‌های آپلودی
├── requirements.txt
├── runtime.txt
├── build.sh
└── manage.py
```

## مدل‌ها

### Product
- name, discription, price, category, picture, star
- is_sale, sale_price

### Category
- name

### Comment
- product, user, rating (1-5), body, created_at, is_active

### Newsletter
- email, created_at, is_active

### Order
- product, customer, quantity, address, phone, date, status

## دسترسی پنل مدیریت

فقط کاربران `is_staff` به پنل مدیریت دسترسی دارند.
