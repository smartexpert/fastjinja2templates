import os
from functools import wraps
from inspect import iscoroutinefunction
from pathlib import Path
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from jinja2.exceptions import TemplateNotFound, UndefinedError
from starlette.datastructures import URL

class FastJinja2Templates(Jinja2Templates):
    def __init__(self, *args, directory_name="templates", **kwargs):
        # Set the default value of the "directory" keyword argument to the path of the module from where init is called + "/directory_name"
        kwargs.setdefault("directory", str(Path(__file__).parent / directory_name))

        # Check if the directory exists, and raise an exception if it does not exist
        if not Path(kwargs["directory"]).exists():
            raise FastJinja2Templates.TemplatesDirectoryNotFound(f'The directory path {Path(kwargs["directory"])} does not exist.')

        # Remove the "functions" keyword argument from kwargs
        functions = kwargs.pop("functions", {})

        # Initialize the Jinja2Templates superclass
        super().__init__(*args, **kwargs)

        # Add the functions from the "functions" keyword argument to self.env.globals
        for key, value in functions.items():
            self.env.globals[key] = value

        # Add the URL class as the "URL" function
        self.env.globals["URL"] = URL

    class TemplatesDirectoryNotFound(Exception):
        pass        

def global_init(*args, **kwargs):
    # Instantiate FastJinja2Templates by passing it all the arguments it received
    global templates
    templates = FastJinja2Templates(*args, **kwargs)
    return templates

# Define template rendering decorator
def template(template_name: str = None):
    def decorator(func, template_name=template_name):

        if template_name is None:
            module_name = os.path.basename(func.__module__).split(".")[-1]
            template_path = f"{module_name}/{func.__name__}.html"
        else:
            template_path = template_name

        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            if iscoroutinefunction(func):
                context = await func(request, *args, **kwargs)
            else:
                context = func(request, *args, **kwargs)
            context["request"] = request
            try:
                return templates.TemplateResponse(template_path, context)
            except TemplateNotFound:
                return {
                    "message": f"Template not found: {template_path} in {templates.env.loader.searchpath[0]}"
                }
            except UndefinedError as error:
                return {
                    "message": f"{error.message} in {template_path}"
                }                
        return wrapper
    return decorator