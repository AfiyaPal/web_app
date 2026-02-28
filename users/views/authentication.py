from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView
)
from django.contrib.auth.forms import (
    PasswordResetForm,
    SetPasswordForm,
)



User = get_user_model()


# ------------------- Register -------------------
def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Basic validation
        if not all([username, email, password1, password2]):
            messages.error(request, "All fields are required.")
            return redirect("users:register")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("users:register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("users:register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("users:register")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Account created successfully!")
        return redirect("users:login")

    return render(request, "accounts/register.html")

# ------------------- Login -------------------
def login_view(request):

    if request.user.is_authenticated:
        return redirect("frontend:index")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        remember = request.POST.get("remember")

        if not username or not password:
            messages.error(request, "Please fill all fields.")
            return redirect("users:login")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            # Remember me
            if not remember:
                request.session.set_expiry(0)  # Browser close = logout
            else:
                request.session.set_expiry(1209600)  # 2 weeks

            messages.success(request, "Welcome back!")

            return redirect("frontend:index")

        messages.error(request, "Invalid credentials.")

    return render(request, "accounts/login.html")

# ------------------- Logout View -------------------
def user_logout(request):
    logout(request)
    messages.info(
        request,
        "You have been logged out successfully."
    )
    return redirect('users:login')


# ------------------- Password Reset Views -------------------
class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    form_class = PasswordResetForm

    def form_valid(self, form):
        messages.success(
            self.request,
            "Password reset link has been sent to your email."
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Error in resetting password. Please try again."
        )
        return super().form_invalid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = SetPasswordForm

    def form_valid(self, form):
        messages.success(
            self.request,
            "Your password has been successfully reset. You can now log in."
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Passwords do not match or do not meet security requirements."
        )
        return super().form_invalid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


