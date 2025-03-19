from django.conf import settings

def show_toolbar(request):
    """
    Function to determine whether to show the toolbar on a given page.
    """
    return settings.DEBUG and \
        settings.ENABLE_DEBUG_TOOLBAR and \
        ((request.META.get("REMOTE_ADDR") in settings.INTERNAL_IPS) or is_host_debug_toolbar_allowed(
            request.get_host()))


def is_host_debug_toolbar_allowed(host):
    for allowed_host in settings.ALLOWED_HOSTS_DEBUG_TOOLBAR:
        if host.endswith(allowed_host):
            return True
    return False