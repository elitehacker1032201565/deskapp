# from django.shortcuts import render, redirect
# from .forms import UserLoginForm, UserRegistrationForm
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
# from .models import CustomUser
# from django.contrib import messages
# from django.http import HttpResponseRedirect
# # from pymongo import MongoClient
# from django.contrib.auth import get_user_model

# User = get_user_model() 

# # client = MongoClient("mongodb://localhost:27017/")  # host uri
# # db = client["admincode"]
# # collection = db["admincode"]

# def home(request):
#     return render(request, 'home.html')

# def user_login(request):
#     error = None
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']

#             user = authenticate(request, username=username, password=password)
#             if user is not None and not user.is_staff:
#                 login(request, user)
#                 return redirect('user_dashboard/')
#         else:
#             error = 'Incorrect login credentials'
#     else:
#         form = UserLoginForm()
    
#     return render(request, 'login.html', {'form': form, 'error': error, 'view_name': 'user_login_view'})    
        

# # def staff_login(request):
# #     error = None
# #     if request.method == 'POST':
# #         form = StaffLoginForm(request.POST)
# #         if form.is_valid():
# #             username = form.cleaned_data['username']
# #             password = form.cleaned_data['password']
# #             admin_code = form.cleaned_data['admin_code']

# #             user = authenticate(request, username=username, password=password)
# #             if user is not None and user.is_staff:
# #                 admin_code_doc = collection.find_one({"code": admin_code})
# #                 if admin_code_doc:
# #                     return redirect('admin_dashboard')  # Adjust redirect URL as needed
# #         else:
# #             error = 'Incorrect login credentials'
# #     else:
# #         form = StaffLoginForm()

# #     return render(request, 'login.html', {'form': form, 'error': error, 'view_name': 'staff_login_view'})

# def user_registration(request):
#     form = UserRegistrationForm()
    
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         # print(request.POST)
#         CustomUser = get_user_model()
#         if form.is_valid():
#             user = CustomUser.objects.create_user('username','email','password1')
#             user.full_name = 'fullname'
#             user = form.save()
#             print(user)  
#             login(request, user)  
#             messages.success(request, 'Your Mod Application has been successfully submitted!')
#             return redirect('user_login')
#     else:
#         form = UserRegistrationForm()

#     return render(request, 'user_registration.html', {'form': form})

# # def staff_registration(request):
# #     if request.method == 'POST':
# #         form = AdminRegistrationForm(request.POST)
# #         print(request.POST)
# #         if form.is_valid():
# #             user = form.save()  
# #             messages.success(request, 'Your Mod Application has been successfully submitted!')
# #             return HttpResponseRedirect('staff_login')
# #     else:
# #         form = AdminRegistrationForm()
# #     return render(request, 'admin_registration.html', {'form': form})

# # def admin_dashboard_view(request):
# #     users = User.objects.all()  # Retrieve all users
# #     return render(request, 'admin_dashboard.html', {'users': users})

# def user_dashboard_view(request):
#     return render(request, 'user_dashboard.html')


from base64 import urlsafe_b64encode
import json
import token
import uuid
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
import requests

from accounts.utils import send_email_token

from .models import CustomUser,UploadedFile
from .filters import CustomUserFilter
from .forms import FileUploadForm
from rest_framework import viewsets,status,generics
from rest_framework.response import Response
from rest_framework import viewsets
from .models import CustomUser, UploadedFile
from .serializers import CustomUserSerializer, UploadedFileSerializer, VerifyAccountSerializer
from djoser.views import TokenCreateView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .emails import *
from .serializers import CustomTokenCreateSerializer

from rest_framework.decorators import api_view
from django.utils.encoding import force_bytes

# from . import UserFile
# from .serializers import UserFileSerializer

User = get_user_model()

def home(request):
    return render(request,"accounts/home.html")

def otp(request):
    if request.method == 'POST':
        email = request.POST['email1']
        otp = request.POST['otp']
        user = CustomUser.objects.filter(email=email)
        if not user.exists():
            messages.error(request,"User does not exist")
            return redirect("home")
        if not user[0].otp == otp:
            messages.error(request,"Invalid otp")
            return redirect("home")
        user[0].is_verified = True
        user[0].save()
        messages.success(request,"Account verified successfully")
        return redirect("signin")
    

    return render(request,"accounts/otp.html")

def signup(request):
    
    if request.method == 'POST':
        public_visibility = False
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['repass']
        public_visibility = request.POST.get('cb1')
        print(password)


        if User.objects.filter(username=username):
            messages.error(request,"Username already in use")
            return redirect("home")
    
        if User.objects.filter(email=email):
            messages.error(request,"email id already in use")
            return redirect("home")
    
        if len(username)>10:
            messages.error(request,"Username must be under 10 characters")

        if password != confirm_password:
            messages.error(request,"Password not matching")
        else:
            if public_visibility == 'on': 
                public_visibility = True
            else:
                public_visibility = False
            
            CustomUser = get_user_model()

            myuser = CustomUser.objects.create_user(username,email,password,email_token=str(uuid.uuid4()))
            
            myuser.first_name = firstname
            myuser.last_name = lastname
            myuser.public_visibility = public_visibility

            myuser.save()
            print(myuser.email_token)
            send_email_token(email,myuser.email_token)
            
            
            send_otp_mail(email)
            return redirect('otp')
          

        if not username.isalnum():
            messages.error(request,"username should be alphanumeric")    
            return redirect("home")

        # myuser = User.objects.create_user(username,email,password)
        
        

    
    return render(request,"accounts/signup.html")

def verify(request,token):
    try:
        obj=CustomUser.objects.get(email_token=token)
        obj.is_verified=True
        obj.save()
        return redirect('signin')
    except Exception as e:
        return HttpResponse('invalid token')


def signin(request):

    if request.method == 'POST':
        
        email = request.POST['email']
        password = request.POST['password']

        print(f"Received credentials: email={email}, password={password}")
    
        user = authenticate(username=email, password=password)

        print(f"Authenticated user: {user}")
        

        if user is not None:
            login(request, user)
            #return render(request,"accounts/userlogin.html")
            return redirect('index')
        else:
            messages.error(request,"Wrong credentials")
            return redirect('home')
            

    return render(request,"accounts/signin.html")


class AuthorsAndSellersView(FilterView):
    model = CustomUser
    template_name = 'authors_and_sellers.html'
    filterset_class = CustomUserFilter
    context_object_name = 'users'

@login_required(login_url='signin')        
def users(request):
    users = User.objects.all()
    print(users)
    return render(request, 'users.html', {'users': users})


@login_required(login_url='signin') 
def index(request):
    users = User.objects.all()
    # print(users)
    return render(request, 'index.html', {'users': users})
    

@login_required
def upload_book(request):
    if request.method == 'POST':
        # book_name = request.POST.get('book_name')
        # book_description = request.POST.get('description')
        # book_file = request.FILES.get('file')
        # book_visibility = request.POST.get('visibility')
        # book_cost = request.POST.get('cost')
        # book_year_published = request.POST.get('year_published')
        
        # print(book_name)
        
        # data={'title':book_name,
        #       'description':book_description,
        #       'visibility':book_visibility,
        #       'cost':book_cost,
        #       'year_published':book_year_published
        #       }
        # file_data={
        #     'file':book_file
        # }
        form = FileUploadForm(request.POST, request.FILES)
        print(form.errors)
        # print(form)
        
        print(form.is_valid())
        if form.is_valid():

            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            messages.success(request, 'Book uploaded successfully.')
            return redirect('uploaded_files')
        else:
            messages.error(request, 'Error uploading the book. Please check the form.')
    else:
        form = FileUploadForm()

    return render(request, 'upload_book.html', {'form': form})

# @login_required
# def uploaded_files(request):
#     user_files = UploadedFile.objects.filter(user=request.user)
#     return render(request, 'uploaded_files.html', {'user_files': user_files})

def uploaded_files(request):
    user_files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'uploaded_files.html', {'user_files': user_files})


def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

def download_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)

    # Assuming the 'file' field in UploadedFile is a FileField
    file_path = uploaded_file.file.path

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
        return response


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class UploadedFileViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

class GenerateToken(APIView):
    def post(self, request):
        if request.method == 'POST':
            email = request.data.get('email')
            password = request.data.get('password')

            print(f"Received credentials: email={email}, password={password}")

            user = authenticate(request, username=email, password=password)

            print(f"Authenticated user: {user}")

            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({'access_token': access_token})
            else:
                return Response({'error': 'Invalid Credentials'}, status=401)
        return Response({'error': 'Invalid request method'}, status=400)


class FileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_files = UserFile.objects.filter(user=request.user)
        serializer = UserFileSerializer(user_files, many=True)
        return Response(serializer.data)
    
# @api_view(['POST'])
# def register_user(request):
#     if request.method == 'POST':
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             send_otp_mail(serializer.data['email'])
#             return redirect('otp')
#         else:
#             return redirect('signup')

# @api_view(['POST'])
# def verify_otp(request):
#     if request.method == 'POST':
#         serializer = VerifyAccountSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.data['email']
#             otp = serializer.data['otp']
#             user = CustomUser.objects.filter(email=email)
#             if not user.exists():
#                 return Response({
#                     'status': 400,
#                     'message': 'User does not exist',
#                     'data': 'invalid email'
#                 }, status=400)
            
#             if not user[0].otp == otp:
#                 return Response({
#                     'status': 400,
#                     'message': 'something went wrong',
#                     'data': 'invalid otp'
#                 }, status=400)
            
#             user[0].is_verified = True
#             user[0].save()
#             return Response({
#                 'status': 200,
#                 'message': 'Account verified successfully',
#                 'data': {}
#             }, status=200)
    
#         return Response({
#             'status': 400,
#             'message': 'Something went wrong',
#             'data': serializer.errors
#         }, status=400)
    
def token_send(request):
    return render(request,'accounts/token_send.html')