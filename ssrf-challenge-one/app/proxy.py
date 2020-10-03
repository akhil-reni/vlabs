import requests
from flask import Flask, request, Response
import socket
import ipaddress
from urllib.parse import urlparse
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)



# allow only internal hosts
def check_ip_hostname(input):
    try:
        socket.inet_aton(input)
        return input, ipaddress.ip_address(input).is_private
    except socket.error:
        try:
            ip = socket.gethostbyname(input)
            return ip, ipaddress.ip_address(ip).is_private
        except Exception as e:
            logger.info(e)
            return False, False
    except Exception as e:
        logger.info(e)
        return False, False




@app.route('/proxy')
def proxy(*args, **kwargs):
    url = request.args.get('url', None)
    if not url:
        return "URL is required", 400
    parsed_uri = urlparse(url)
    ip, _go_ahead = check_ip_hostname(parsed_uri.hostname)
    if _go_ahead:
        try:
            resp = requests.request(
                method=request.method,
                url=url,
                headers={key: value for (key, value) in request.headers if key != 'Host'},
                data=request.get_data(),
                cookies=request.cookies,
                allow_redirects=False)
            excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
            headers = [(name, value) for (name, value) in resp.raw.headers.items()
                       if name.lower() not in excluded_headers]

            response = Response(resp.content, resp.status_code, headers)
            return response
        except Exception as e:
            logger.info(e)
    return "something went wrong!", 400

if __name__ == '__main__':
    app.run(debug=True)
