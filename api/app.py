import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

with open("./secrets.json", "r") as fp:
    GOOGLE_CREDS = json.load(fp)

GOOGLE_WELL_KNOWN = "https://accounts.google.com/.well-known/openid-configuration"

oauth = OAuth()

oauth.register(
    name="google",
    client_id=GOOGLE_CREDS["google_client_id"],
    client_secret=GOOGLE_CREDS["google_client_secret"],
    server_metadata_endpoint=GOOGLE_WELL_KNOWN,
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    access_token_url="https://oauth2.googleapis.com/token",
    scope="openid profile"
)

ALLOWED_ORIGINS = ["https://login.hax0rsearch.com:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*"
)

app.add_middleware(
    SessionMiddleware,
    secret_key="123"
)

@app.get("/login/google")
async def login(request: Request):
    return await oauth.create_client("google").authorize_redirect(
        request,
        "https://login.hax0rsearch.com:8081/login/google/callback"
    )

@app.get("/login/google/callback")
async def login(request: Request):
    token = await oauth.create_client("google").authorize_access_token(request)
    redirect = RedirectResponse(
        "https://login.hax0rsearch.com:8080",
        headers = {
            "set-cookie": f"token=${json.dumps(token)}; domain=login.hax0rsearch.com:8080;"
        }
    )
    return redirect
