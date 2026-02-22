from django import template

register = template.Library()


@register.simple_tag
def query_string(request, **kwargs):
    params = request.GET.copy()
    if "page" in params:
        params.pop("page")

    for k, v in kwargs.items():
        if v in (None, "", False):
            params.pop(k, None)
        else:
            params[k] = v
    return params.urlencode()
