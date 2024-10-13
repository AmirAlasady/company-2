from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.views.static import serve

from company import settings


# media files protection 
def protected_media_view(request, path):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    # Add additional permission checks here if needed
    return serve(request, path, document_root=settings.MEDIA_ROOT)