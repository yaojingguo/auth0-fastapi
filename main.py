"""main.py
Python FastAPI Auth0 integration example
"""

from fastapi import FastAPI, Depends, Response, status
from fastapi.security import HTTPBearer

from .utils import VerifyToken

token_auth_scheme = HTTPBearer()

# Creates app instance
app = FastAPI()


@app.get("/api/public")
def public():
    """No access token required to access this route"""

    result = {
        "status": "success",
        "msg": (
            "Hello from a public endpoint! You don't need to be "
            "authenticated to see this."
        ),
    }
    return result


@app.get("/api/private")
def private(response: Response, token: str = Depends(token_auth_scheme)):  # 👈 updated code
    """A valid access token is required to access this route"""

    print(f"token: {token}")
    result = VerifyToken(token.credentials).verify()  # 👈 updated code

    # 👇 new code
    if result.get("status"):
       response.status_code = status.HTTP_400_BAD_REQUEST
       return result
    # 👆 new code

    return result
