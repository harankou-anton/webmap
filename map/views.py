from django.db.models import Q
from django.shortcuts import render
from profiles.models import Layer

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        layers = Layer.objects.filter(Q(layer_accsses__access_code=0) & Q(layer_accsses__user_id=request.user.id))
        return render(request, "map.html", {"layers": layers})
    else:
        return render(request, "map.html")