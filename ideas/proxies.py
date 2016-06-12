import re

PROXY_REGEX = re.compile(r"^([\d\.:]+)")

def read_proxies(proxy_file = 'proxy.txt'):
    proxies = []
    with open(proxy_file) as proxy_source:
        for proxy in proxy_source:
            match = PROXY_REGEX.match(proxy)
            if match:
                proxies.append(match.group(1))
    return proxies
