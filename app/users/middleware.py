import re

from django.conf import settings
from django.contrib.auth.decorators import login_required

# modified source:
#   http://stackoverflow.com/questions/2164069/best-way-to-make-djangos-login-required-the-default#answer-2164224

from django.http import HttpResponseRedirect


class RequireLoginMiddleware(object):
    """
    Middleware component that wraps the login_required decorator around
    matching URL patterns. To use, add the class to MIDDLEWARE_CLASSES and
    define LOGIN_REQUIRED_URLS and LOGIN_REQUIRED_URLS_EXCEPTIONS in your
    settings.py. For example:
    ------
    LOGIN_REQUIRED_URLS = (
        r'/topsecret/(.*)$',
    )
    LOGIN_REQUIRED_URLS_EXCEPTIONS = (
        r'/topsecret/login(.*)$',
        r'/topsecret/logout(.*)$',
    )
    ------
    LOGIN_REQUIRED_URLS is where you define URL patterns; each pattern must
    be a valid regex.

    LOGIN_REQUIRED_URLS_EXCEPTIONS is, conversely, where you explicitly
    define any exceptions (like login and logout URLs).
    """
    def __init__(self, get_response):
        self.get_response = get_response  # require django 1.11 !
        self.required = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS)
        self.exceptions = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS)

    def __call__(self, request):  # require django 1.11 !
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # No need to process URLs if user already logged in
        if request.user.is_authenticated():
            return None

        # An exception match should immediately return None
        for url in self.exceptions:
            if url.match(request.path):
                return None

        # Requests matching a restricted URL pattern are returned
        # wrapped with the login_required decorator
        for url in self.required:
            if url.match(request.path):  # TODO: TEST IT!
                """
                By default login_required has attribute ?next= ... this trick removes this GET data
                """
                # login_required_without_next = login_required(view_func,
                #                                              redirect_field_name=None)(request,
                #                                                                        *view_args,
                #                                                                        **view_kwargs)
                # return login_required_without_next
                # ### login_required_without_next returns the same as HttpResponseRedirect("/")
                return HttpResponseRedirect(settings.LOGIN_URL)

        # Explicitly return None for all non-matching requests
        return None
