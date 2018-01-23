from flask import json, Response


def format_response(response: Response):
    """Format JSON response"""
    status_code = response.status_code
    success = (status_code >= 200) and (status_code <= 299)
    content_type = response.headers.get('content-type', 'plain/text')
    is_json = content_type == 'application/json'
    body = json.loads(response.get_data()) if is_json else response.get_data().decode('utf-8')
    message = None
    data = None

    if isinstance(body, str):
        message = body
    elif isinstance(body, dict):
        if 'message' in body:
            message = body.pop('message')

        if 'data' in body:
            data = body.pop('data')
        else:
            data = body
    else:
        data = body

    response.headers['content-type'] = 'application/json'
    response.set_data(json.dumps(dict(success=success,
                                      status_code=status_code,
                                      message=message,
                                      data=data)))

    return response
