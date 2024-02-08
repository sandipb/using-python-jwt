.PHONY: genkeys

genkeys: genkeys-openssl genkeys-ssh genshared

genkeys-openssl:
	@echo "\n*** Generating RSA keys using openssl\n"
	rm -f rsa-private.pem rsa-public.pem
	openssl genrsa -out rsa-private.pem 2048
	openssl rsa -in rsa-private.pem -pubout -outform PEM  -out rsa-public.pem

genkeys-ssh:
	@echo "\n*** Generating RSA keys using ssh-keygen\n"
	rm -f id_rsa id_rsa.pub
	ssh-keygen -t rsa -f id_rsa -N ""

genshared:
	@echo "\n*** Generating shared secret\n"
	rm -f shared-secret
	openssl rand -hex 32 > shared-secret