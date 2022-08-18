import requests

def get_external_ip():
    """Get your external IP address as string.
    Uses httpbin(1): HTTP Request & Response Service
    """
    return requests.get("http://httpbin.org/ip").json().get('origin')

def duckdns_update(domains, token, newIp=None, verbose=False):
    """Update duckdns.org Dynamic DNS record.
    Args:
        domains (str): The DuckDNS domains to update as comma separated list.
        token (str): An UUID4 provided by DuckDNS for your user.
        verbose (bool): Returns info about whether or not IP has been changed as
            well as if the request was accepted.
    Returns:
        "OK" or "KO" depending on success or failure. Verbose adds IP and change
        status as well.
    """
    params = {
        "domains": domains,
        "token": token,
        "ip": newIp if not None else get_external_ip(),
        "verbose": verbose
    }
    r = requests.get("https://www.duckdns.org/update", params)
    return r.text.strip().replace('\n', ' ')
