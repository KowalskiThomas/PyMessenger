import hashlib
import hmac

def validate_hub_signature(app_secret, request_payload, hub_signature_header):
    try:
        hash_method, hub_signature = hub_signature_header.split('=')
    except:
        pass
    else:
        digest_module = getattr(hashlib, hash_method)
        hmac_object = hmac.new(str(app_secret), str(request_payload), digest_module)
        generated_hash = hmac_object.hexdigest()
        if hub_signature == generated_hash:
            return True
    return False


def generate_appsecret_proof(access_token, app_secret):
    hmac_object = hmac.new(bytearray(app_secret, 'utf8'), str(access_token).encode('utf8'), hashlib.sha256)
    generated_hash = hmac_object.hexdigest()
    return generated_hash
