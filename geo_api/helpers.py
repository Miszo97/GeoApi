import socket


def getIP(domain):
    """
    This method returns the first IP address string
    that responds as the given domain name
    """
    try:
        data = socket.gethostbyname(domain)
        ip = str(data)
        return ip
    except Exception:
        # fail gracefully!
        return False
