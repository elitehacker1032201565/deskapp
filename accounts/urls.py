# from django.contrib import admin
# from django.urls import path
# from . import views

# urlpatterns = [
    
#     path('', views.home, name='home'),
#     path('user_login/', views.user_login, name='user_login'),
#     # path('staff_login/', views.staff_login, name='staff_login'),
#     path('user_registration/', views.user_registration, name='user_registration'),
#     # path('staff_registration/', views.staff_registration, name='staff_registration'),
#     # path('admin_dashboard', views.admin_dashboard_view, name='staff_dashboard'), 
#     path('user_login/user_dashboard/', views.user_dashboard_view, name='user_dashboard'),   

# ]

from django.db import router
from django.urls import path,include
from .import views
from .views import AuthorsAndSellersView, token_send
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, UploadedFileViewSet, GenerateToken


router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'uploaded_files', UploadedFileViewSet,basename='uploaded_files')

urlpatterns = [
    path('', views.home, name='home'),
    # path("register", views.register_user, name="register"),
    # path("verify", views.verify_otp, name="verify"),

    path("otp", views.otp, name="otp"),
    path('signup',views.signup, name='signup'),
    path('signin',views.signin, name='signin'),
    path('index',views.index, name='index'),
    path('users',views.users, name='users'),
    path('authors_and_sellers/', AuthorsAndSellersView.as_view(), name='authors_and_sellers'),
    path('upload_book',views.upload_book,name='upload_book'),
    path('upload_files',views.uploaded_files,name='uploaded_files'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('api/', include(router.urls)),
    path('api1/generate-token/', GenerateToken.as_view(), name='generate_token'),
    # path('api2/file_view/', FileView.as_view(), name='file_view'),
    path('logout/', views.custom_logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
