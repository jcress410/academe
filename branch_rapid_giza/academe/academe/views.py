from academe import traversal
from pyramid.view import view_config


@view_config(context=traversal.Root, renderer='main.html')
def my_view(request):
    return {'project': 'academe'}
