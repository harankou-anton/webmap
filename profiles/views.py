from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from profiles.forms import LoginForm, RegisterForm, UploadedData, UpdateData
from profiles.upload_update_delete import uploading_style, uploading_process, updating_process, delete_layer
from profiles.models import Layer, LayerAccess, Accsess
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


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
    form_layer = UpdateData()
    form_style = UploadedData()

    if request.POST.get("upd-layer"):
        form_layer = UpdateData(request.POST, request.FILES)
        if form_layer.is_valid():
            updating_process(request.FILES['file'], layer_id)
            return redirect("layer_list")

    if request.POST.get("upd-style"):
        form_style = UploadedData(request.POST, request.FILES)

        if form_style.is_valid():
            uploading_style(request.FILES['file'], form_style.cleaned_data['name'], layer_id)
            return redirect("layer_list")

    context = {"details": details, "form_layer": form_layer, "form_style": form_style}
    return render(request, "details.html", context=context)


def delete_page(request, layer_id):
    delete_layer(layer_id)
    return HttpResponseRedirect(reverse('layer_list'))


def share_layer(request, layer_id):
    details = get_object_or_404(Layer, layer_id=layer_id)
    levels = Accsess.objects.exclude(access_code=0)
    accesses = LayerAccess.objects.filter(layer_id_id=layer_id).exclude(access_code_id=0)
    if request.POST.get("share-btn"):
        email_field = request.POST.get("email-input")
        level = request.POST.get("level")
        search_user = User.objects.get(email=email_field)
        LayerAccess.objects.create(access_code_id=level, layer_id_id=layer_id,
                                   user_id_id=search_user.id)
        return redirect("layer_list")
    context = {"details": details, "levels": levels, "accesses": accesses}
    return render(request, "share.html", context)
