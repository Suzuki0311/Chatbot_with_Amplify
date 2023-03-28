import hashlib
import hmac
import base64
# import const
from . import const



def verify_request(event):
    x_line_signature = event["headers"].get("x-line-signature") or event["headers"].get("X-Line-Signature")
    body = event["body"]

    # Generate the signature using HMAC-SHA256
    hash = hmac.new(const.LINE_CHANNEL_SECRET.encode('utf-8'), body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash)

    # Compare the signature from the request headers with the generated signature
    if signature != x_line_signature.encode():
        raise Exception("Request verification failed. Request came from a non-LINE server source.")