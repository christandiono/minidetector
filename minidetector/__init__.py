from django.conf import settings

from minidetector.useragents import search_strings

class Middleware(object):
    @staticmethod
    def process_request(request):
        """ Adds a "mobile" attribute to the request which is True or False
            depending on whether the request should be considered to come from a
            small-screen device such as a phone or a PDA"""

        # defaults (we assume this is a desktop)
        request.is_android_device = False
        request.is_ios_device = False
        request.is_simple_device = False
        request.is_touch_device = False
        request.is_webkit = False
        request.is_webos_device = False
        request.is_wide_device = True
        request.is_windows_phone_device = False

        if request.META.has_key("HTTP_X_OPERAMINI_FEATURES"):
            #Then it's running opera mini. 'Nuff said.
            #Reference from:
            # http://dev.opera.com/articles/view/opera-mini-request-headers/

            request.is_simple_device = True

            return None

        if request.META.has_key("HTTP_ACCEPT"):
            s = request.META["HTTP_ACCEPT"].lower()
            if 'application/vnd.wap.xhtml+xml' in s:
                # Then it's a wap browser

                request.is_simple_device = True

                return None

        if request.META.has_key("HTTP_USER_AGENT"):
            # This takes the most processing. Surprisingly enough, when I
            # Experimented on my own machine, this was the most efficient
            # algorithm. Certainly more so than regexes.
            # Also, Caching didn't help much, with real-world caches.

            s = request.META["HTTP_USER_AGENT"].lower()

            if 'applewebkit' in s:
                request.is_webkit = True

            if 'ipad' in s:
                request.is_ios_device = True
                request.is_touch_device = True
                request.is_wide_device = True

                return None

            if 'iphone' in s or 'ipod' in s:
                request.is_ios_device = True
                request.is_touch_device = True
                request.is_wide_device = False

                return None

            if 'android' in s:
                request.is_android_device = True
                request.is_touch_device = True
                request.is_wide_device = False # TODO add support for andriod tablets

                return None

            if 'webos' in s:
                request.is_webos_device = True
                request.is_touch_device = True
                request.is_wide_device = False # TODO add support for webOS tablets

                return None

            if 'windows phone' in s:
                request.is_windows_phone_device = True
                request.is_touch_device = True
                request.is_wide_device = False

                return None

            for ua in search_strings:
                if ua in s:
                    request.is_simple_device = True
                    return None

        return None

    @staticmethod
    def process_response(request, response):
        response['Vary'] = 'User-Agent' # add Vary header
        return response


def detect_mobile(view):
    """ View Decorator that adds a "mobile" attribute to the request which is
        True or False depending on whether the request should be considered
        to come from a small-screen device such as a phone or a PDA"""

    def detected(request, *args, **kwargs):
        Middleware.process_request(request)
        return Middleware.process(request, view(request, *args, **kwargs))
    detected.__doc__ = "%s\n[Wrapped by detect_mobile which detects if the request is from a phone]" % view.__doc__
    return detected

__all__ = ['Middleware', 'detect_mobile']
