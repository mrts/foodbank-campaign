def get_ip_address(request):
    # may also come from X-HTTP-FORWARDED-FOR
    return request.META.get('REMOTE_ADDR')

def get_user_agent(request):
    return request.META.get('HTTP_USER_AGENT')[:255]
