#!/bin/bash
uvicorn app:app --port 8081 --host 172.31.0.78 --ssl-keyfile ./privatekey.pem --ssl-keyfile-password 123456 --ssl-certfile ./public.crt
