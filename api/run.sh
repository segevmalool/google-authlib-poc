#!/bin/bash
uvicorn app:app --port 8081 --host 172.31.0.78 --ssl-keyfile ./privatekey.pem --ssl-keyfile-password ${keypass} --ssl-certfile ./public.crt
