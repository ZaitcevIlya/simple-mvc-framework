from pprint import pprint


def parse_input_data(data: str):
    result = {}
    if data:
        params = data.split('&')
        for i in params:
            k, v = i.split('=')
            result[k] = v
    return result


class GetRequests:
    """GET requests processor"""
    @staticmethod
    def get_request_params(environ):
        query_string = environ['QUERY_STRING']
        request_params = parse_input_data(query_string)
        return request_params


class PostRequests:
    """POST requests processor"""
    @staticmethod
    def get_wsgi_input_data(environ):
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0

        data = environ['wsgi.input'].read(content_length) \
            if content_length > 0 else b''
        return data

    @staticmethod
    def parse_wsgi_input_data(data: bytes):
        result = {}
        if data:
            print(f'raw data: {data}')
            data_str = data.decode(encoding='utf-8')
            print(f'Decoded string - {data_str}')
            result = parse_input_data(data_str)
        return result

    def get_request_params(self, environ):
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)
        return data
