import sys
import json
import base64
import time
from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import urlencode
import os
# Check for Python version
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    timer = time.perf_counter  # High precision timer for Python 3
else:
    timer = time.clock  # Older timer for Python 2

# API Key and Secret Key for Baidu Speech API
API_KEY = '3VBaT71woIq8N34aFwawFo03'
SECRET_KEY = 'js8neaOXZcnU9yOkJWAyLpfydaxZkwww'

# Default settings for audio file
AUDIO_FILE = '16k.pcm'  # Supported formats: pcm, wav, amr
FORMAT = AUDIO_FILE[-3:]  # Extract file extension
CUID = '123456PYTHON'  # User unique identifier
RATE = 16000  # Fixed sample rate for audio

# Baidu API endpoint and scope
ASR_URL = 'http://vop.baidu.com/server_api'
DEV_PID = 1537  # Set the language model (PID for Mandarin)
SCOPE = 'audio_voice_assistant_get'  # Define scope for ASR ability

# Error class for handling specific API errors
class DemoError(Exception):
    pass

"""  TOKEN start """
TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'

def fetch_token():
    """Fetch access token from Baidu API using client credentials"""
    params = {
        'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': SECRET_KEY
    }
    # 禁用代理设置
    # 禁用系统代理
    os.environ['HTTP_PROXY'] = ''
    os.environ['HTTPS_PROXY'] = ''
    os.environ['http_proxy'] = ''
    os.environ['https_proxy'] = ''

    post_data = urlencode(params).encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        response = urlopen(req)
        result_str = response.read().decode()
        result = json.loads(result_str)

        if 'access_token' in result and 'scope' in result:
            if SCOPE and SCOPE not in result['scope'].split(' '):
                raise DemoError('scope is not correct')
            print(f"SUCCESS WITH TOKEN: {result['access_token']} EXPIRES IN SECONDS: {result['expires_in']}")
            return result['access_token']
        else:
            raise DemoError('API_KEY or SECRET_KEY may be incorrect: access_token or scope not found in response')

    except URLError as err:
        print(f"Token fetch failed: {err}")
        raise

"""  TOKEN end """

def read_audio_file(file_path):
    """Read and return the audio file in binary format"""
    with open(file_path, 'rb') as f:
        return f.read()

def send_speech_to_asr(token, audio_data, length):
    """Send audio data to Baidu ASR service and get the response"""
    speech = base64.b64encode(audio_data).decode('utf-8')  # Convert audio data to base64

    params = {
        'dev_pid': DEV_PID,
        'format': FORMAT,
        'rate': RATE,
        'token': token,
        'cuid': CUID,
        'channel': 1,
        'speech': speech,
        'len': length
    }
    post_data = json.dumps(params)
    req = Request(ASR_URL, post_data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')

    try:
        begin = timer()
        response = urlopen(req)
        result_str = response.read().decode('utf-8')
        print(f"Request time cost {timer() - begin:.6f}s")
        return result_str
    except URLError as err:
        print(f"ASR request failed: {err}")
        raise

if __name__ == '__main__':
    try:
        # Step 1: Fetch access token
        # '24.aea73dc1504834293bc8d88554dca89e.2592000.1734082789.282335-116227376'
        # 24.124a6b6b26d31593110110da553f5c7e.2592000.1734159964.282335-116227376
        token = '24.aea73dc1504834293bc8d88554dca89e.2592000.1734082789.282335-116227376'

        # Step 2: Read audio file
        audio_data = read_audio_file(AUDIO_FILE)
        if len(audio_data) == 0:
            raise DemoError(f"File {AUDIO_FILE} length is 0 bytes")

        # Step 3: Send audio to ASR service
        result = send_speech_to_asr(token, audio_data, len(audio_data))

        # Step 4: Output result and save to file
        print(result)
        with open("result.txt", "w") as f:
            f.write(result)

    except DemoError as e:
        print(f"Error: {str(e)}")
