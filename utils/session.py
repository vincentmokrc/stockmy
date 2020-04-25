import requests
import time
from urllib.parse import urlencode

class _SendRequest:
    def __init__(
        self,
        retry_count=3,
        pause=0.1,
        timeout=30,
        session=None,
        freq=None,
        ):
        
        if not isinstance(retry_count, int) or retry_count < 0:
            raise ValueError("'retry_count' must be integer larger than 0")
        self.retry_count = retry_count
        self.pause = pause
        self.timeout = timeout
        self.pause_multiplier = 1
        self.session = self._init_session(session, retry_count)
        self.freq = freq

    @staticmethod
    def _init_session(session, retry_count=3):
        if session is None:
            session = requests.Session()
        # do not set requests max_retries here to support arbitrary pause
        return session
    
    def close(self):
        self.session.close()

    def _get_response(self, url, params = None, headers = None):
        pause = self.pause
        last_response_text = ""
        for _ in range(self.retry_count + 1):
            response = self.session.get(url, params=params, headers=headers)
            if response.status_code == requests.codes.ok:
                return response

            if response.encoding:
                last_response_text = response.text.encode(response.encoding)
            time.sleep(pause)

            pause *= self.pause_multiplier

            if self._output_error(response):
                break

        if params is not None and len(params) > 0:
            url = url + "?" + urlencode(params)
        msg = "Unable to read URL: {0}".format(url)
        if last_response_text:
            msg += "\nResponse Text:\n{0}".format(last_response_text)

    def download_response(self, url, save_path):
        res = self._get_response(url)
        
        if is_downloadable(res):
            open(save_path, 'wb').write(res.content)

    @staticmethod
    def is_downloadable(response):
        """
        Does the url contain a downloadable resource
        """
        header = response.headers
        content_type = header.get('content-type')
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False

        return True