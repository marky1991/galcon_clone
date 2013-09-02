def banner_context_processor(request):
    show_banner = request.COOKIES.get("show_banner")
    return { 'show_banner' : show_banner }
