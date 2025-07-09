from urllib.parse import urlparse

BLACKLIST_DOMAINS = ['www.google.com']

def is_valid(url):
    domain = urlparse(url).netloc
    return not any(bad in domain for bad in BLACKLIST_DOMAINS)

def score_url(url, date=None):
    # Dummy score: tu peux ajouter des critères de fraîcheur, réputation, etc.
    return 1
