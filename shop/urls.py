from django.urls import path , include
from . import views 
from .views import login_user

urlpatterns = [
    
    path('' , views.helloworld , name="home"),
    path('about/' , views.about , name="about"),
    path('contact/' , views.contact , name="contact"),
    path('terms/' , views.terms , name="terms"),
    path('login/' , views.login_user , name="login"),
    path('logout/' , views.logout_user , name="logout"),
    path('signup/' , views.signup_user , name = "signup"),
    path('product/<int:pk>' , views.product , name = "product"),
    path('category/<str:cat>' , views.category , name = "category"),
    path('newsletter/subscribe/' , views.newsletter_subscribe , name = "newsletter_subscribe"),
    path('product/<int:pk>/comment/' , views.add_comment , name = "add_comment"),
    path('profile/' , views.profile , name = "profile"),
    path('search/' , views.search , name = "search"),
    path('switch-language/' , views.switch_language , name = "switch_language"),

    # Admin Panel
    path('admin-panel/' , views.admin_dashboard , name = "admin_dashboard"),
    path('admin-panel/product/add/' , views.admin_product_add , name = "admin_product_add"),
    path('admin-panel/product/<int:pk>/edit/' , views.admin_product_edit , name = "admin_product_edit"),
    path('admin-panel/product/<int:pk>/delete/' , views.admin_product_delete , name = "admin_product_delete"),
    path('admin-panel/category/add/' , views.admin_category_add , name = "admin_category_add"),
    path('admin-panel/category/<int:pk>/edit/' , views.admin_category_edit , name = "admin_category_edit"),
    path('admin-panel/category/<int:pk>/delete/' , views.admin_category_delete , name = "admin_category_delete"),
    path('admin-panel/products/' , views.admin_products_list , name = "admin_products_list"),
    path('admin-panel/categories/' , views.admin_categories_list , name = "admin_categories_list"),
    path('admin-panel/users/' , views.admin_users_list , name = "admin_users_list"),
    path('admin-panel/user/<int:pk>/toggle/' , views.admin_user_toggle , name = "admin_user_toggle"),
    path('admin-panel/user/<int:pk>/delete/' , views.admin_user_delete , name = "admin_user_delete"),
    path('admin-panel/comments/' , views.admin_comments_list , name = "admin_comments_list"),
    path('admin-panel/comment/<int:pk>/toggle/' , views.admin_comment_toggle , name = "admin_comment_toggle"),
    path('admin-panel/comment/<int:pk>/delete/' , views.admin_comment_delete , name = "admin_comment_delete"),
]
