def authenticate(request):
    return True
    if not request.user.is_anonymous() and \
           request.user.is_active:
        return True
    else:
        return False