


class UrlpathRecorMw(object):
    """记录用户访问的网址"""
    EXCLUDE_URLS = ['/user/login/', '/user/logout/', '/user/register/']


    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if request.path not in UrlpathRecorMw.EXCLUDE_URLS and request.method == "GET" and not request.is_ajax():
            request.session['url_path'] = request.path
            # print(request.path)
