# @ Time    : 2020/5/22 21:22
# @ Author  : JuRan

from urllib.parse import urlparse, urljoin
from flask import request


def is_safe_url(target):

    ref_url = urlparse(request.host_url)

    test_url = urlparse(urljoin(request.host_url, target))

    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# is_safe_url('http://127.0.0.1:5000/test/')
