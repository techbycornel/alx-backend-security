from django.http import HttpResponseForbidden
from django.utils import timezone
from ipware import get_client_ip
from django.core.cache import cache
from .models import RequestLog, BlockedIP
import requests

def get_geo_info(ip):
    cached = cache.get(ip)
    if cached:
        return cached

    url = f"https://ipinfo.io/{ip}/json"
    try:
        res = requests.get(url).json()
    except:
        res = {}

    data = {
        "country": res.get("country", ""),
        "city": res.get("city", "")
    }

    cache.set(ip, data, 86400)  # 24hrs
    return data

class IPTrackingMiddleware:   # <-- THIS NAME MUST MATCH SETTINGS.PY
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)

        # Block blacklisted IPs
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP is blocked.")

        # Log Request
        geo = get_geo_info(ip)
        RequestLog.objects.create(
            ip_address=ip,
            timestamp=timezone.now(),
            path=request.path,
            country=geo.get("country"),
            city=geo.get("city"),
        )

        return self.get_response(request)
