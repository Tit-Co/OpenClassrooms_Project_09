from django.shortcuts import redirect


def index(request):
    """
    Method to redirect to accounts application login page
    Args:
        request (HttpRequest): Http request

    Returns:
        An HttpResponseRedirect to accounts application login page.
    """
    return redirect(to='../log_in/')
