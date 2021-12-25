
from server import TCPSocketServerContext


def get_registered_clients(context: TCPSocketServerContext):
    if 'holepunch_registered_clients' not in context.server_context:
        context.server_context['holepunch_registered_clients'] = dict()
    return context.server_context['holepunch_registered_clients']
        