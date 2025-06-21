"""
Controller for handling authentication requests.
"""
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv

from rest_fastapi.core.config import Settings, get_settings
from rest_fastapi.security import auth
from rest_fastapi.security.schemas import Token

router = APIRouter()


@cbv(router)
class LoginController:
    """Resource for handling the token generation endpoint."""

    @router.post("/login/token", response_model=Token, tags=["Authentication"])
    def post(
        self,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        settings: Annotated[Settings, Depends(get_settings)],
    ):
        """Provide an access token for a valid user."""
        user = settings.USER_LOGIN.get(form_data.username)
        if not user or user["password"] != form_data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_SECONDS
        )
        
        # Pass the injected settings object to the create function
        access_token = auth.create_access_token(
            data={"sub": form_data.username},
            settings=settings,  # Pass the settings object
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}






# """
# Controller for handling authentication requests.

# This module defines the resource that processes user login and issues
# JWT access tokens.
# """
# from datetime import timedelta
# from typing import Annotated

# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from fastapi_utils.cbv import cbv
# from fastapi_utils.inferring_router import InferringRouter

# from rest_fastapi.core.config import Settings, get_settings
# from rest_fastapi.security import auth
# from rest_fastapi.security.schemas import Token

# # A mock user database for demonstration purposes.
# FAKE_USERS_DB = {"testuser": {"password": "testpassword"}}

# router = InferringRouter()


# @cbv(router)
# class LoginController:
#     """
#     Resource for handling the token generation endpoint.

#     Methods
#     -------
#     post(form_data)
#         Processes POST requests to authenticate a user and return a JWT.
#     """

#     @router.post("/login/token", response_model=Token, tags=["Authentication"])
#     def post(
#         self,
#         form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
#         settings: Annotated[Settings, Depends(get_settings)],
#     ):
#         """
#         Provide an access token for a valid user.

#         Parameters
#         ----------
#         form_data : OAuth2PasswordRequestForm
#             The user's credentials.
#         settings : Settings
#             The application settings, injected by FastAPI.

#         Returns
#         -------
#         Token
#             A JSON object containing the access token and token type.
#         """
#         user = FAKE_USERS_DB.get(form_data.username)
#         if not user or user["password"] != form_data.password:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Incorrect username or password",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
        
#         access_token_expires = timedelta(
#             minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
#         )
        
#         access_token = auth.create_access_token(
#             data={"sub": form_data.username},
#             expires_delta=access_token_expires,
#             settings=settings
#         )
#         return {"access_token": access_token, "token_type": "bearer"}
