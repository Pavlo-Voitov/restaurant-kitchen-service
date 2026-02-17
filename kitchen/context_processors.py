from django.db.models import Count
from .models import DishType, Cook
from django.db.models import Q


def sidebar_search(request):
    type_query = (request.GET.get("type_q") or "").strip()
    cook_query = (request.GET.get("cook_q") or "").strip()

    types = DishType.objects.annotate(dish_count=Count("dishes")).order_by("name")
    cooks = Cook.objects.annotate(cook_count=Count("dishes")).order_by("username")

    if type_query:
        types = types.filter(name__icontains=type_query)

    if cook_query:
        cooks = cooks.filter(
            Q(username__icontains=cook_query) |
            Q(first_name__icontains=cook_query) |
            Q(last_name__icontains=cook_query)
        )

    return {
        "sidebar_types": types,
        "type_query": type_query,
        "sidebar_cooks": cooks,
        "cook_query": cook_query,
    }
