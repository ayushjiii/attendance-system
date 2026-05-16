import math
from django.conf import settings


def get_client_ip(request):
    """
    Get the real IP address of the user making the request.
    
    Why check X-Forwarded-For?
    When a server sits behind a proxy or load balancer,
    the real user IP is in this header, not REMOTE_ADDR.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # Can contain multiple IPs like "client, proxy1, proxy2"
        # We want the first one (the real client)
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_office_ip(ip_address):
    """
    Check if an IP address is in the allowed office network.
    """
    if not ip_address:
        return False

    allowed_ips = getattr(settings, 'ALLOWED_OFFICE_IPS', [])

    for allowed in allowed_ips:
        if '/' in allowed:
            # Subnet check: compare everything before the last dot
            network_prefix = allowed.rsplit('.', 1)[0]
            if ip_address.startswith(network_prefix):
                return True
        else:
            if ip_address == allowed:
                return True

    return False


def calculate_distance_meters(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two GPS coordinates in meters.
    Uses the Haversine formula (accounts for Earth's curvature).
    
    Arguments:
        lat1, lon1: First point (float)
        lat2, lon2: Second point (float)
    
    Returns:
        Distance in meters (float)
    """
    R = 6371000  # Earth's radius in meters

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def is_within_office_radius(latitude, longitude):
    """
    Return True if the given GPS coordinates are within
    the allowed office radius (defined in settings).
    
    If GPS settings are not configured, returns True (skips check).
    """
    office_lat = getattr(settings, 'OFFICE_LATITUDE', None)
    office_lon = getattr(settings, 'OFFICE_LONGITUDE', None)
    radius = getattr(settings, 'OFFICE_RADIUS_METERS', 100)

    # If office GPS not configured, skip the check
    if office_lat is None or office_lon is None:
        return True

    distance = calculate_distance_meters(
        float(latitude), float(longitude),
        float(office_lat), float(office_lon)
    )
    return distance <= radius


def get_device_info(request):
    """
    Extract browser and OS info from the HTTP User-Agent header.
    Stored for audit purposes so admin can see what device was used.
    
    Example output:
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0...'
    """
    return request.META.get('HTTP_USER_AGENT', 'Unknown device')