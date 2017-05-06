import re

from django.conf import settings

from django.http import HttpResponseRedirect


class RequireLoginMiddleware(object):
    """
    Middleware replacing the login_require decorator,
    prevent to access for non authenticated user into locations which are not specified in LOGIN_REQUIRED_URLS_EXCEPTIONS
    """
    def __init__(self, get_response):
        self.get_response = get_response  # require django 1.11 !
        self.exceptions = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS)

    def __call__(self, request):  # require django 1.11 !
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # No need to process URLs if user already logged in
        if request.user.is_authenticated():
            return None

        # If non authenticated user are allowed to access exception locations return None
        for url in self.exceptions:
            if url.match(request.path):
                return None

        # Explicitly redirect for all other requests
        return HttpResponseRedirect(settings.LOGIN_URL)
