from django.http import JsonResponse


def live(request):
    """Health check endpoint."""
    return JsonResponse({"status": "ok"})
