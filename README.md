# FastAPI Multi-Auth Template

This project is a template for building FastAPI APIs with JWT and simple token authentication, using a modular, class-based resource structure. It is designed to be easily extended for new projects.

## Quick Start

1. **Install dependencies**  
   ```sh
   poetry install
   ```
2. **Configure environment**
    Copy `secrets/.env.example` to `secrets/.env` and fill in your secrets, just for development. For production add your environment variables to system's environment or external services like `Secret Mannager` (AWS, GCP...)

3. **Run the app**
    ```sh
    uvicorn rest_fastapi.main:app --reload
    ```
4. **API Docs**
    Visit http://localhost:8000/docs for Swagger interactive documentation.

## Authentication Overview

- JWT Auth: Standard OAuth2 password flow, token issued at `/login/token`.
- Simple Token Auth: Static API token via Authentication header.
- Public Routes: No authentication required.


## How to Add a New Protected Route

1. **Create a Controller**
    Add a new method to a controller class in `rest_fastapi/controllers/`.
    Example: Add to `rest_fastapi/controllers/protected.py`:

    ```python
    # ...existing code...

    from rest_fastapi.security import auth
    from rest_fastapi.security.schemas import TokenData

    @cbv(router)
    class MyProtectedController:
        @router.get("/my/protected/endpoint")
        def my_protected_method(
            self,
            current_user: Annotated[TokenData, Depends(auth.auth_jwt)],
        ):
            return {"message": f"Hello {current_user.username}, this is a protected endpoint."}
    # ...existing code...
    ```
    - Use `Depends(auth.auth_jwt)` for JWT protection.
    - Use `Depends(auth.auth_token)` for simple token protection.

2. **Register the Controller**

    Make sure your controller's router is included in `rest_fastapi/routes/api.py`:

    ```python
    # ...existing code...
    from rest_fastapi.controllers import my_controller

    def init_api_routes(app: FastAPI):
        app.include_router(login.router)
        app.include_router(protected.router)
        app.include_router(my_controller.router)  # Add your router here
    # ...existing code...
    ```

3. **Test Your Route**
    Add tests in `tests/` using TestClient and the provided fixtures. See `tests/test_protected.py` for examples.


## Environment Variables

See `secrets/.env.example` for all required variables:

- SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_SECONDS
- SIMPLE_API_TOKEN
- USER_LOGIN (JSON dict of users)


## Extending the Template

- Add new controllers in `controllers/`.
- Add new routers in `routes/api.py`.
- Add new authentication dependencies in `security/auth.py`.
- Add new settings in `core/config.py`.


## Running Tests
```sh
poetry run pytest
```

## Docker

- Build and run with Docker Compose:
```sh
docker-compose up --build
```



## References

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Pytest Documentation](https://docs.pytest.org/en/stable/contents.html)



## License

MIT License