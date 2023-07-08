from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from profiles.forms import LoginForm, RegisterForm, UploadedData, UpdateData
from profiles.upload_data import uploading_process
from profiles.update_data import updating_process
from profiles.models import Layer
from django.db.models import Q


# Create your views here.
def auth(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request=request,
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is None:
                return HttpResponse("BadRequest", status=400)
            login(request, user)
            return redirect("map")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User(email=form.cleaned_data["email"], username=form.cleaned_data["email"])
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("map")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("map")


def upload_file(request):
    if request.method == "POST":
        form = UploadedData(request.POST, request.FILES)
        if form.is_valid():
            uploading_process(request.FILES['file'], form.cleaned_data['name'], request.user.id)
            return redirect("map")
    else:
        form = UploadedData()
    return render(request, "upload_page.html", {"form": form})


def layer_list(request):
    data = Layer.objects.filter(Q(layer_accsses__access_code=0) & Q(layer_accsses__user_id=request.user.id))
    return render(request, "list_layer.html", {"data": data})


def details(request, layer_id):
    details = get_object_or_404(Layer, layer_id=layer_id)
    form = UpdateData()
    if request.method == "POST":
        form = UpdateData(request.POST, request.FILES)
        if form.is_valid():
            updating_process(request.FILES['file'], layer_id)
            return redirect("map")

    return render(request, "details.html", {"details": details, "form": form})
