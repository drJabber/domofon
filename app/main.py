from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.api.routes.api import router as api_router
from app.core.config import (ALLOWED_HOSTS, API_PREFIX_V1, DEBUG,
    PROJECT_NAME, VERSION, OPENAPI_DOCS_PATH, 
    OPENAPI_JSON_URL, OPENAPI_REDOC_PATH,
    ALLOWED_HOSTS_FOR_PATHS,
)

from app.core.events import create_start_app_handler, create_stop_app_handler
from app.services.middlewares import AllowedPathsMiddleware

def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION, 
          openapi_url=OPENAPI_JSON_URL, docs_url=OPENAPI_DOCS_PATH, redoc_url=OPENAPI_REDOC_PATH)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_middleware(
        AllowedPathsMiddleware,
        patterns=ALLOWED_HOSTS_FOR_PATHS
    )



    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix=API_PREFIX_V1)

    application.mount(path='',app=StaticFiles(directory='app/static/html'), name='static')

    return application


app = get_application()
