from django.http import Http404

from .models import Group


class GroupExistsOr404Middleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """ 
        request.path is like /xxx/yyy/.../
        This method check if first parameter is 'group' and second is valid integer
        if yes then check if group with given id exists (if group exists pass if doesn't raise 404 exception)
        else does nothing
        """
        # split_path[0] is always empty!
        split_request = request.path.split('/', 3)

        if split_request[1] == 'group' and len(split_request) >= 3:
            print("test")
            try:
                group_id = int(split_request[2])
            except ValueError:
                return None

            if not Group.objects.filter(id=group_id).exists():
                raise Http404

        return None
