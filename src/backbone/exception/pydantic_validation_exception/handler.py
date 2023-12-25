from typing import List, Dict

from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from backbone.api.translator.translator import translate


def validation_exception_handler(request: Request, exception: RequestValidationError):
    errors: List[Dict] = exception.errors()
    new_errors = []
    for error in errors:
        location = ".".join([str(location) for location in error['loc']])
        type_ = error['type']
        context = error.get('ctx', {})
        message: str = 'pydantic.' + error['type']
        message = translate(message, **context)
        new_errors.append({'loc': location, 'message': message, 'type': type_})
    return JSONResponse({'message': "Inputted data was invalid", 'errors': new_errors}, status_code=422)