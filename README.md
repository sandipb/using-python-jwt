# How to use Python for encoding and decoding JWTs

This is a simple example of how to use Python to encode and decode JWTs. It uses the `PyJWT` library for encoding and decoding JWTs.
This demonstrates using both OpenSSH and OpenSSL keys for signing JWTs.

## Pre-requisites

```shell-session
pip install pyjwt[crypto]
```

## Generate some keys to be used for signing JWTs

This will generate some test keys for shared secret and RSA keys from OpenSSH and OpenSSL.

```shell-session
$ make genkeys

*** Generating RSA keys using openssl

rm -f rsa-private.pem rsa-public.pem
openssl genrsa -out rsa-private.pem 2048
openssl rsa -in rsa-private.pem -pubout -outform PEM  -out rsa-public.pem
writing RSA key

*** Generating RSA keys using ssh-keygen

rm -f id_rsa id_rsa.pub
ssh-keygen -t rsa -f id_rsa -N ""
Generating public/private rsa key pair.
Your identification has been saved in id_rsa
Your public key has been saved in id_rsa.pub
The key fingerprint is:
SHA256:vJoObruvvbyNNxmzfN4Ug4Hrc3f4s3y8AycmMkFCR14 sbhattacharya@somehost
The key's randomart image is:
+---[RSA 3072]----+
|      ...o E     |
|       .oo.      |
|        +..      |
|       . o o     |
|        S o o    |
|       .o+ . B . |
|    .  .+=+ * =. |
|   ..+ =*o.+ +..o|
|   .=*@+.+. . +=o|
+----[SHA256]-----+

*** Generating shared secret

rm -f shared-secret
openssl rand -hex 32 > shared-secret
```

## Running the code

```shell-session
$ ./jwt-test.py 
*** Sample payload:
{'iss': 'jwt-test.py', 'sub': 'sbhattacharya', 'name': 'Sandip Bhattacharya', 'nickname': 'sbhattacharya', 'aud': 'https://example.com', 'exp': 1707426737, 'iat': 1707423137}

*** Token signed by shared secret:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJqd3QtdGVzdC5weSIsInN1YiI6InNiaGF0dGFjaGFyeWEiLCJuYW1lIjoiU2FuZGlwIEJoYXR0YWNoYXJ5YSIsIm5pY2tuYW1lIjoic2JoYXR0YWNoYXJ5YSIsImF1ZCI6Imh0dHBzOi8vZXhhbXBsZS5jb20iLCJleHAiOjE3MDc0MjY3MzcsImlhdCI6MTcwNzQyMzEzN30.o-XdNSEE0FmViPdGi5mex6cZ9MfGEugdexONpppgAlc

*** Token signed by RSA key(OPENSSH):
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJqd3QtdGVzdC5weSIsInN1YiI6InNiaGF0dGFjaGFyeWEiLCJuYW1lIjoiU2FuZGlwIEJoYXR0YWNoYXJ5YSIsIm5pY2tuYW1lIjoic2JoYXR0YWNoYXJ5YSIsImF1ZCI6Imh0dHBzOi8vZXhhbXBsZS5jb20iLCJleHAiOjE3MDc0MjY3MzcsImlhdCI6MTcwNzQyMzEzN30.sGtgRqv2dXfC2m6ehV_uXX-wYl2UYhYMXK5saV6Dmum0xiYbHPCdEoDDk5X8I_WTlHL0FPwnbq47t10ky0CXoSWFOyE4hetl7vPJf-KFn1T962DDI1MjbJZluIiYXqTQ3HhMQ8GokxtAxWf63dxZDIqOXpEg41Vj-gmpxe1BX0AZV0vVPSCJHVZbrrNzrYFBsQ2l7Ld_IHqroqOagQZizgnMraYeulgNI_SyNq1OY77hcO99MoOLrhQa-3LQxbgq6FN8XnmTL31CZAvVm1Qk7x2BhbORV279eDV1AJcpycpi_kvkxbBmXRhLWGG4BERUHkrU3pkk0t0PSAa6hQRLk3l076_pg4Z3-3lIRqRxt6X6EWm8vp0y9JunZMaQ-Z3x_b1iQA8hJc8iL2E_KIlggxqILUtgzdTyhNAS7WZyTeHLup5aOMz5jQd4RgbZ0jpXMdqlcEw06FeFFBJDqfUWO9KHz1OhSrFBIZ9Rx7hzIZ3_Zi7BDtf5oW8zMTQ-uuj3

*** Token signed by RSA key(OPENSSL):
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJqd3QtdGVzdC5weSIsInN1YiI6InNiaGF0dGFjaGFyeWEiLCJuYW1lIjoiU2FuZGlwIEJoYXR0YWNoYXJ5YSIsIm5pY2tuYW1lIjoic2JoYXR0YWNoYXJ5YSIsImF1ZCI6Imh0dHBzOi8vZXhhbXBsZS5jb20iLCJleHAiOjE3MDc0MjY3MzcsImlhdCI6MTcwNzQyMzEzN30.lfCVsa6enUp5prsaycHpkZ30_quW-7XAS4jW02y6sajn4r7XBeZnnt50Krlbhf6DNLq9OX0b4e4v5nlTOR1M7vvNWUs3vvT70osgLcvV21JZf5azNr3AOUkGShKNTfs7L74qzGVircAsvZkNTs_tCdJ_2jKg0UxsDr5AUaDFV4-UYKwfWK8hpu8CSAMBRFZiBc-TRuMiY69MoAXHjfVUnSS0Cj6l3iGsI-WR3C-tUtUHFxLH_e_A-R0YtXGGSH29uWYlBHapYIvLxNq00BpqKZn2EvKXXrQY2-Fcbt8U2QibHbcQlj1-wg5tCNGpHk2Z8-VBFOSzTEMbG9kDO26-7A

*** Now you can verify the token signature


*** Enter token to verify: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJqd3QtdGVzdC5weSIsInN1YiI6InNiaGF0dGFjaGFyeWEiLCJuYW1lIjoiU2FuZGlwIEJoYXR0YWNoYXJ5YSIsIm5pY2tuYW1lIjoic2JoYXR0YWNoYXJ5YSIsImF1ZCI6Imh0dHBzOi8vZXhhbXBsZS5jb20iLCJleHAiOjE3MDc0MjY3MzcsImlhdCI6MTcwNzQyMzEzN30.o-XdNSEE0FmViPdGi5mex6cZ9MfGEugdexONpppgAlc

*** [INFO] Token signature algorithm: HS256
*** [INFO] Token expiration: 2024-02-08 16:12:17-05:00 (in 0:59:52.511284)
*** Verifying and decoding via shared secret:
{'iss': 'jwt-test.py', 'sub': 'sbhattacharya', 'name': 'Sandip Bhattacharya', 'nickname': 'sbhattacharya', 'aud': 'https://example.com', 'exp': 1707426737, 'iat': 1707423137}

*** Enter token to verify: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJqd3QtdGVzdC5weSIsInN1YiI6InNiaGF0dGFjaGFyeWEiLCJuYW1lIjoiU2FuZGlwIEJoYXR0YWNoYXJ5YSIsIm5pY2tuYW1lIjoic2JoYXR0YWNoYXJ5YSIsImF1ZCI6Imh0dHBzOi8vZXhhbXBsZS5jb20iLCJleHAiOjE3MDc0MjY3MzcsImlhdCI6MTcwNzQyMzEzN30.lfCVsa6enUp5prsaycHpkZ30_quW-7XAS4jW02y6sajn4r7XBeZnnt50Krlbhf6DNLq9OX0b4e4v5nlTOR1M7vvNWUs3vvT70osgLcvV21JZf5azNr3AOUkGShKNTfs7L74qzGVircAsvZkNTs_tCdJ_2jKg0UxsDr5AUaDFV4-UYKwfWK8hpu8CSAMBRFZiBc-TRuMiY69MoAXHjfVUnSS0Cj6l3iGsI-WR3C-tUtUHFxLH_e_A-R0YtXGGSH29uWYlBHapYIvLxNq00BpqKZn2EvKXXrQY2-Fcbt8U2QibHbcQlj1-wg5tCNGpHk2Z8-VBFOSzTEMbG9kDO26-7A

*** [INFO] Token signature algorithm: RS256
*** [INFO] Token expiration: 2024-02-08 16:12:17-05:00 (in 0:59:39.321347)
*** Verifying and decoding via ssh public key:
Invalid signature

*** Verifying and decoding via openssl public key:
{'iss': 'jwt-test.py', 'sub': 'sbhattacharya', 'name': 'Sandip Bhattacharya', 'nickname': 'sbhattacharya', 'aud': 'https://example.com', 'exp': 1707426737, 'iat': 1707423137}

*** Enter token to verify: 
```

## References

- <https://auth0.com/blog/how-to-handle-jwt-in-python/>
