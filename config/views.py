from django.db import connection
from django.http import JsonResponse


def health(request):
    """Report whether the app can reach its database."""
    try:
        connection.ensure_connection()
    except Exception:
        return JsonResponse(
            {"status": "error", "code": 503, "detail": "database unavailable"},
            status=503,
        )
    return JsonResponse({"status": "ok", "code": 200})
