from typing import Optional
from urllib import parse

from django import urls


def build_url(
    view_name: str,
    url_kwargs: Optional[dict] = None,
    query_params: Optional[dict] = None,
) -> str:
    url_kwargs = url_kwargs or {}

    url = urls.reverse(view_name, kwargs=url_kwargs)
    if query_params:
        query_params_string = parse.urlencode(query_params, doseq=True)
        url = f"{url}?{query_params_string}"

    return url
