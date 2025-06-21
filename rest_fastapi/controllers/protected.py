"""
Controllers for example protected routes using dependency injection.
"""

from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi_utils.cbv import cbv

from rest_fastapi.security import auth
from rest_fastapi.security.schemas import TokenData

router = APIRouter(tags=["Protected Routes"])


@cbv(router)
class ProtectedRoutesController:
    """
    Resource for endpoints protected by different auth schemes.
    """

    @router.get("/examples/protected/jwt-only")
    def get_jwt_only(
        self,
        current_user: Annotated[TokenData, Depends(auth.auth_jwt)],
    ):
        """Handle GET request protected exclusively by JWT."""
        return {
            "message": f"Hello {current_user.username}, you are "
                       "authenticated via JWT."
        }

    @router.get("/examples/protected/simple-token-only")
    def get_simple_token_only(
        self,
        token: Annotated[str, Depends(auth.auth_token)],
    ):
        """Handle GET request protected by a simple API token."""
        return {"message": "You are authenticated via a simple API token."}

    # @router.get("/examples/protected/any-auth")
    # def get_any_auth(
    #     self,
    #     auth_result: Annotated[dict, Depends(auth.auth_general)],
    # ):
    #     """Handle GET request protected by either auth method."""
    #     method = auth_result.get("method")
    #     user_obj = auth_result.get("user")

    #     if method == "jwt" and user_obj:
    #         user_display = user_obj.username
    #     else:
    #         user_display = "API user"

    #     return {
    #         "message": f"Hello {user_display}! You have been authenticated "
    #                    f"using: {method}."
    #     }


@cbv(router)
class UnprotectedController:
    """Resource for an unprotected endpoint."""

    @router.get("/examples/public/unprotected")
    def get(self):
        """Handle GET request."""
        return {
            "message": "This endpoint is public and requires no authentication."
        }
