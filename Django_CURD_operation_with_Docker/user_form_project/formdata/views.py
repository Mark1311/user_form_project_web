from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import UserData
import re



def is_valid_name(name: str) -> bool:
    # Allow only letters (A-Z, a-z) and spaces. Trim whitespace.
    if not name:
        return False
    return bool(re.match(r'^[A-Za-z ]+$', name.strip()))

def is_valid_phone(phone: str) -> bool:
    # Basic: only digits and length between 7 and 15 (adjust as needed)
    if not phone:
        return False
    return phone.isdigit() and 7 <= len(phone) <= 15

def home(request):
    errors = []  # collect all validation messages
    # Keep previous values so user doesn't have to retype everything on error
    prev = {"name": "", "email": "", "phone": ""}

    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        email = (request.POST.get("email") or "").strip()
        password = request.POST.get("password") or ""
        phone = (request.POST.get("phone") or "").strip()

        prev["name"] = name
        prev["email"] = email
        prev["phone"] = phone

        # Name validation
        if not is_valid_name(name):
            errors.append("Name should contain only letters and spaces (no numbers or special characters).")

        # Email format validation
        try:
            validate_email(email)
        except ValidationError:
            errors.append("Invalid email format! Please enter a valid email (example: name@example.com).")

        # Phone validation (optional but recommended)
        if not is_valid_phone(phone):
            errors.append("Phone must contain only digits and be 7 to 15 characters long.")

        # Duplicate email check (only if email format ok)
        if not errors:
            if UserData.objects.filter(email=email).exists():
                errors.append("This email is already registered!")

        # If no errors, save and redirect
        if not errors:
            UserData.objects.create(
                name=name,
                email=email,
                password=password,  # later: hash this
                phone=phone
            )
            return redirect("home")

    users = UserData.objects.all()
    return render(request, "home.html", {"users": users, "errors": errors, "prev": prev})


def delete_user(request, user_id):
    user = get_object_or_404(UserData, id=user_id)
    user.delete()
    return redirect("home")