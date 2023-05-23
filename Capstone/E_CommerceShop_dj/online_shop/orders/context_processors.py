from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from user_auth.models import Profile
from .utils import cartData


def base_template_variables_context_processor(request):
    data = cartData(request)
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return {"profile": profile, 'user': request.user, 'items': data["items"], 'cartItems': data["cartItems"]}
    else:
        return {'profile': {}, 'user': 'AnonymousUser', 'items': data["items"], 'cartItems': data["cartItems"]}
    