import os
from functools import wraps
from inspect import iscoroutinefunction, currentframe, getmodule
from pathlib import Path
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from jinja2.exceptions import TemplateNotFound, UndefinedError
from starlette.datastructures import URL

error_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Error</title>
    <style>
        body {
            display: flex;
            align-items: center;
            justify-content: center;
        }
    </style>
</head>
<body>
    <h1>{{ FastJinja2TemplatesError }}</h1>
</body>
</html>
"""

class FastJinja2Templates(Jinja2Templates):
    def __init__(self, *args, root_directory, directory_name="templates", **kwargs):
        # Set the default value of the "directory" keyword argument to the path of the module from where init is called + "/directory_name"
        kwargs.setdefault("directory", str(root_directory / directory_name))

        # Check if the directory exists, and raise an exception if it does not exist
        if not Path(kwargs["directory"]).exists():
            raise FastJinja2Templates.TemplatesDirectoryNotFound(f'The directory path {Path(kwargs["directory"])} does not exist.')

        # Check if the error.html file exists, and create it if it does not
        error_template_path = Path(kwargs["directory"]) / "error.html"
        if not error_template_path.exists():
            with open(error_template_path, "w") as error_template_file:
                error_template_file.write(error_template)

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
    global templates

    # Get the module object for the calling frame
    frame = currentframe().f_back
    module = getmodule(frame)

    # Instantiate FastJinja2Templates using the arguments and the module's parent directory
    templates = FastJinja2Templates(*args, **kwargs, root_directory=Path(module.__file__).parent)

    return templates

# Define template rendering decorator
def template(_func=None, * ,template_name: str = None):
    """
    This function is a decorator that is used to render the output of a function as a Jinja2 template.
    
    Arguments:
    _func (callable): The decorated function.
    template_name (str, optional): The path to the template that will be rendered. If not specified, the module and function name will be used as the path.
    
    The decorated function should return a dictionary of context variables that will be passed to the template.
    If the decorated function is an async function, it will be called asynchronously. Otherwise, it will be called synchronously.
    If there is an error when rendering the template, the error template will be rendered and the error message will be passed as a context variable.
    """
    def decorator(func, template_name:str=_func):
        if template_name is None:
            # if no template is specified, use the name of the module and function as the template path
            module_name = os.path.basename(func.__module__).split(".")[-1]
            template_path = f"{module_name}/{func.__name__}.html"
        else:
            # use the provided template name as the path
            template_path = template_name

        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            if iscoroutinefunction(func):
                # if the function is an async function, call it asynchronously
                context = await func(request, *args, **kwargs)
            else:
                # if the function is not an async function, call it synchronously
                context = func(request, *args, **kwargs)
            # add the request object to the context
            context["request"] = request
            try:
                # render the template using the specified path and the context
                return templates.TemplateResponse(template_path, context)
            except TemplateNotFound:
                # if the template is not found, render the error template and pass the error message as a context variable
                return templates.TemplateResponse("error.html", {"FastJinja2TemplatesError": f"Template not found: {template_path} in {templates.env.loader.searchpath[0]}","request": request, **context}, status_code=500)
            except UndefinedError as error:
                # if there is an error when rendering the template, render the error template and pass the error message as a context variable
                return templates.TemplateResponse("error.html", {"FastJinja2TemplatesError": f"{error.message} in {template_path}","request": request, **context}, status_code=500)               
        return wrapper

    if callable(_func):
        # if _func is a function, call the decorator with the function and set template_name to None
        return decorator(_func,template_name=None)
    else:
        # if _func is not a function, return the decorator function
        return decorator