from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import UserProfile
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, UserProfileForm


@require_http_methods(["GET", "POST"])
def auth(request):
    """Trang kết hợp Đăng nhập & Đăng ký"""
    if request.user.is_authenticated:
        return redirect('home')
    
    login_form = UserLoginForm()
    register_form = UserRegistrationForm()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'login':
            login_form = UserLoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, f'Chào mừng {user.username}!')
                    if user.is_superuser or user.is_staff:
                        return redirect('admin_dashboard')
                    return redirect(request.GET.get('next', 'home'))
                else:
                    messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
        
        elif action == 'register':
            register_form = UserRegistrationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                UserProfile.objects.create(user=user, role='user')
                
                login(request, user)
                messages.success(request, 'Đăng ký và đăng nhập thành công!')
                return redirect('home')
    
    context = {
        'login_form': login_form,
        'register_form': register_form,
    }
    return render(request, 'accounts/auth.html', context)


def register_success(request):
    """Trang thành công đăng ký"""
    return render(request, 'accounts/register_success.html')


@require_http_methods(["GET", "POST"])
def register(request):
    """Đăng ký tài khoản với phân trang"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Tạo UserProfile
            profile = UserProfile.objects.create(user=user, role='user')
            messages.success(request, 'Đăng ký thành công!')
            return redirect('register_success')
        else:
            # Gộp tất cả lỗi để hiển thị
            all_errors = []
            for field, errors in form.errors.items():
                for error in errors:
                    all_errors.append(f"{error}")
            context = {
                'form': form,
                'errors': all_errors,
            }
            return render(request, 'accounts/register.html', context)
    else:
        form = UserRegistrationForm()
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Đăng nhập"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Chào mừng {user.first_name or user.username}!')
                if user.is_superuser or user.is_staff:
                    return redirect('admin_dashboard')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    else:
        form = UserLoginForm()
    
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@require_http_methods(["GET"])
def logout_view(request):
    """Đăng xuất"""
    logout(request)
    messages.success(request, 'Bạn đã đăng xuất thành công.')
    return redirect('home')


@login_required
def profile(request):
    """Xem và cập nhật profile"""
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, role='user')
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Cập nhật profile thành công!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def change_password(request):
    """Đổi mật khẩu"""
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password1 = request.POST.get('new_password1', '')
        new_password2 = request.POST.get('new_password2', '')
        
        if not request.user.check_password(old_password):
            messages.error(request, 'Mật khẩu cũ không đúng.')
        elif new_password1 != new_password2:
            messages.error(request, 'Mật khẩu mới không trùng khớp.')
        elif len(new_password1) < 8:
            messages.error(request, 'Mật khẩu phải có ít nhất 8 ký tự.')
        else:
            request.user.set_password(new_password1)
            request.user.save()
            messages.success(request, 'Đặt lại mật khẩu thành công!')
            return redirect('login')
    
    return render(request, 'accounts/change_password.html')
