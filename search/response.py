from review import serializers


def responseFactory(result):
    code = 200
    msg = 'OK'
    if result is None:
        code = '404'
        msg = 'Not Found'
    return {
            'status': code,
            'message': msg,
            'data': result
        }
