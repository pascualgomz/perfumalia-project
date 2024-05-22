# myapp/context_processors.py

def current_template(request):
    return {
        'current_template': request.get_full_path()
    }
