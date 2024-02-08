#!/usr/bin/env python3

import os
import pwd
from pathlib import Path
import sys
import time
from datetime import datetime
import logging

import jwt
from cryptography.hazmat.primitives import serialization

# https://github.com/jpadilla/pyjwt/issues/120#issuecomment-87101534
# Audience should match while decoding the token
AUDIENCE = "https://example.com"
TOKEN_DURATION_SECONDS = 60 * 60

# Key files
SSH_PRIVATE_KEY_FILE = "id_rsa"
SSH_PUBLIC_KEY_FILE = "id_rsa.pub"
OPENSSL_PRIVATE_KEY_FILE = "rsa-private.pem"
OPENSSL_PUBLIC_KEY_FILE = "rsa-public.pem"
SHARED_SECRET_FILE = "shared-secret"

SECRET = Path(SHARED_SECRET_FILE).read_text().strip()


def generate_payload():
    "Generate a JWT payload with some standard claims"
    current_user = pwd.getpwuid(os.getuid())
    # Registered claims: https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-token-claims#registered-claims
    return {
        # Issuer of the JWT
        "iss": os.path.basename(sys.argv[0]),
        # user identifier or subject of this token
        "sub": current_user.pw_name,
        "name": current_user.pw_gecos,
        "nickname": current_user.pw_name,
        # Recipient for which the JWT is intended
        "aud": AUDIENCE,
        "exp": int(time.time()) + TOKEN_DURATION_SECONDS,
        "iat": int(time.time()),
    }


def sign(payload, secret, algorithm):
    return jwt.encode(payload, secret, algorithm)


def verify(token, secret, algorithm):
    try:
        return jwt.decode(token, secret, algorithms=[algorithm], audience=AUDIENCE)
    except jwt.InvalidSignatureError:
        return "Invalid signature"
    except jwt.ExpiredSignatureError:
        return "Expired signature"
    except jwt.DecodeError:
        return "Decode error"
    except jwt.InvalidTokenError as e:
        return "Invalid token: {}".format(e)
    except Exception as e:
        return "Error: " + str(e)


def get_ssh_private_key(private_key_path):
    return serialization.load_ssh_private_key(Path(private_key_path).read_bytes(), password=None)


def get_openssl_private_key(private_key_path):
    return serialization.load_pem_private_key(Path(private_key_path).read_bytes(), password=None)


def get_ssh_public_key(public_key_path):
    return serialization.load_ssh_public_key(Path(public_key_path).read_bytes())


def get_openssl_public_key(public_key_path):
    return serialization.load_pem_public_key(Path(public_key_path).read_bytes())


def token_details(token):
    "Return the token details"
    headers, body = (
        jwt.get_unverified_header(token),
        jwt.decode(token, verify=False, options={"verify_signature": False}),
    )

    details = {"alg": headers.get("alg"), "exp": body.get("exp")}
    if details["exp"] is not None:
        details["exp_date"] = datetime.fromtimestamp(details["exp"]).astimezone()
    return details


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    payload = generate_payload()
    print(f"*** Sample payload:\n{payload}")
    print()

    token = sign(payload, SECRET, "HS256")
    print(f"*** Token signed by shared secret:\n{token}")
    print()

    token = sign(payload, get_ssh_private_key(SSH_PRIVATE_KEY_FILE), "RS256")
    print(f"*** Token signed by RSA key(OPENSSH):\n{token}")
    print()

    token = sign(payload, get_openssl_private_key(OPENSSL_PRIVATE_KEY_FILE), "RS256")
    print(f"*** Token signed by RSA key(OPENSSL):\n{token}")
    print()

    print("*** Now you can verify the token signature\n")
    print()

    while True:
        user_token = input("*** Enter token to verify: ")
        if user_token.strip() == "":
            break
        print()
        token_desc = token_details(user_token)
        token_alg = token_desc["alg"]
        print("*** [INFO] Token signature algorithm:", token_alg)
        print(
            "*** [INFO] Token expiration: {} (in {})".format(
                token_desc["exp_date"],
                token_desc["exp_date"] - datetime.now().astimezone(),
            )
        )

        if token_alg in ["HS256", "RS256"]:
            if token_alg == "HS256":
                shared_verify = verify(user_token, SECRET, "HS256")
                print(f"*** Verifying and decoding via shared secret:\n{shared_verify}")
            else:
                logging.debug("Loading SSH and OPENSSL public keys")
                public_key_ssh = get_ssh_public_key(SSH_PUBLIC_KEY_FILE)
                public_key_openssl = get_openssl_public_key(OPENSSL_PUBLIC_KEY_FILE)

                ssh_verify = verify(user_token, public_key_ssh, "RS256")
                openssl_verify = verify(user_token, public_key_openssl, "RS256")

                print(f"*** Verifying and decoding via ssh public key:\n{ssh_verify}")
                print()
                print(f"*** Verifying and decoding via openssl public key:\n{openssl_verify}")

        else:
            print("\n*** [ERROR] Invalid token signature algorithm !!!\n")

        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
