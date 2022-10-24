from auth0.v3.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier, TokenValidationError
import os

domain = os.environ.get("AUTH0_DOMAIN", None)
client_id = os.environ.get("AUTH0_CLIENT_ID", None)
audience = os.environ.get("AUTH0_AUDIENCE", None)

jwks_url = 'https://{}/.well-known/jwks.json'.format(domain)
issuer = 'https://{}/'.format(domain)
sv = AsymmetricSignatureVerifier(jwks_url)  # Reusable instance

def getAuthToken(headers):
    auth_header = headers.get("Authorization", None)
    if not auth_header:
        print("No header")
        return None
    auth_header_components = auth_header.split()

    if auth_header_components[0].lower() != "bearer":
        print("Bad Auth Header Type")
        return None
    elif len(auth_header_components) <= 1:
        print("Bad Auth Header Length (1)")
        return None
    elif len(auth_header_components) > 2:
        print("Bad Auth Header Length (>2)")
        return None

    token = auth_header_components[1]
    return token

def authenticate_user(token) -> bool:
    try:
        tv = TokenVerifier(signature_verifier=sv, issuer=issuer, audience=client_id)
        tv.verify(token)
    except TokenValidationError as err:
        print(err)
        return False
    return True
