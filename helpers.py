

from django.core.exceptions import PermissionDenied
def is_ceo(request):
    if not request.user.is_authenticated:
        raise PermissionDenied("Login & Try Again")
    if not request.user.is_ceo:
        raise PermissionDenied("Only CEO members allowed")
    


def is_employee(request):
    if not request.user.is_authenticated:
        raise PermissionDenied("Login & Try Again")
    if request.user.is_ceo:
        raise PermissionDenied("Only employees team members allowed")
    if request.user.is_active != True:
        raise PermissionDenied("user is not active")
    