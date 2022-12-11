## Introduction

The fastjinja2templates package makes it easy to use Jinja2 templates with FastAPI. It offers the following benefits:

- A simple and intuitive decorator syntax for converting FastAPI endpoints to render Jinja templates.
- Convenient debugging tools for quickly identifying and resolving issues with templates, such as incorrect template paths or undefined functions or variables.
- The ability to globally inject custom functions into Jinja2 templates, making it easy to reuse common code across your templates.
- The option to customize the error template, allowing you to provide a consistent experience for your users when errors occur.
- The ability to create dynamically generated links within Jinja templates using the url_for method of the FastAPI request object, along with the include_query_parameters method of the startlette.datastructures.URL class. This allows you to easily create links using route names, path parameters, and query parameters.

With fastjinja2templates, you can easily add dynamic content to your FastAPI applications using Jinja templates. It makes template management simple and helps you provide a seamless user experience even in the face of errors.

## Installation

To install the fastjinja2templates package, you can use either pip or poetry.

*Note that you must install fastapi and jinja2 packages before hand to avoid any errors during installation.*

**Installing with pip**
To install the package using pip, run the following command:

``pip install fastjinja2templates``

**Installing with poetry**

To install the package using poetry, run the following command:

``poetry add fastjinja2templates``

## Quick Start

To get started with fastjinja2templates, you need to create a templates directory and place your Jinja templates in it. The default location of the templates directory is templates in the current directory from where `global_init` is called, but you can specify a custom directory using the directory argument.

Once you have created the templates directory, you can use the `global_init` function to initialize the FastJinja2Templates object and make it available to your FastAPI application.

Here is a minimal example of using fastjinja2templates with default values:

```
# Import the global_init function and template decorator from the fastjinja2templates package
from fastapi import FastAPI, Request
from fastjinja2templates import global_init, template

# Create a FastAPI app
app = FastAPI()

# Initialize the global templates object with default values
global_init()

# Define a FastAPI endpoint that uses the template decorator to render a Jinja template
@app.get("/")
@template()
def index(request: Request):
    return {"message": "Hello, world!"}
```

In the above example, the `main/index.html` template will be used to render the response for the `/` endpoint. The `template` decorator is used to convert the `index` function, which **must include** the `request` argument and **return a dictionary**, to a FastAPI endpoint that renders the `main/index.html` template with the data returned by the `index` function. The name of the template is inferred from the name of the function and the module it is defined in.

Assuming the code segment exists in a file called `main.py`, the `main/index.html` template must be placed in a folder named `main` inside the default `templates` directory, which is located in the same directory as `main.py`.

For more information about customizing the templates directory and injecting custom functions into Jinja2 templates, see the usage section of the documentation.
## The global_init function

The global_init function is part of the fastjinja2templates package and is used to initialize the FastJinja2Templates object for use in a FastAPI application.

To use global_init, you need to import it from the fastjinja2templates package and call it with the appropriate arguments:

```
from fastjinja2templates import global_init

# Initialize the global templates object
global_init(
    directory="path/to/templates/directory",  # optional, default is "templates" in current directory
    directory_name="directory_name",  # optional, default is "templates"
    functions={
        "my_function": my_function,
        "my_other_function": my_other_function,
    },  # optional
)
```
The global_init function accepts the following arguments:

- directory: (Optional) The path to the directory where the templates are stored. If this is not specified, the default value is the "templates" directory in the current directory from where global_init is called.
- directory_name: (Optional) The name of the directory where the templates are stored. This is used to construct the default template path for the template decorator. If directory is specified, this argument is ignored. Otherwise, the default value is "templates".
- functions: (Optional) A dictionary of functions that should be available in the Jinja2 environment. The keys of the dictionary are the function names, and the values are the function objects.

After calling global_init, you can use the template decorator from the fastjinja2templates package to specify which templates should be used to render the responses of your path operation functions. For example:

```
from fastjinja2templates import template

@template("my_template.html")
async def my_path_operation_function(request: Request):
    # ...
    return {"my_variable": 42}
```

Alternatively, if you don't specify a template name, the template decorator will use the name of the path operation function and the name of the module it is defined in to construct the path of the template. For example, if the function is defined in a module named `my_module.py`, and the function is named `my_path_operation_function`, the template decorator will use the template at the path `my_module/my_path_operation_function.html` by default.

When the template decorator is applied to a path operation function, it will automatically render the specified template with the context returned by the function and return a HTMLResponse object. It will also add the request object to the context so that it is available in the template.

If an error occurs while rendering the template (e.g. if the template is not found or a variable is undefined), the template decorator will render an error page using the error.html template and return a HTMLResponse object with a status code of 500 (Internal Server Error).
## Customizing the Templates Directory

By default, the `global_init` function will look for Jinja2 templates in the "templates" directory that is located in the same directory as the module where the `global_init` function is called. You can customize the templates directory by passing the directory or directory_name arguments to the `global_init` function.

Here is an example of how to use the `global_init` function to specify the templates directory using the directory argument:

```
from fast_jinja2_templates import global_init
# Use a custom templates directory
global_init(directory="my_templates")
```

In this example, the `global_init` function is called with the `directory` argument, so it will use the specified templates directory instead of the default directory.

Alternatively, you can specify the templates directory using the `directory_name` argument, which specifies the name of the templates directory that should be located in the same directory as the module where the `global_init` function is called:

Copy code
```
from fast_jinja2_templates import global_init
# Use a custom templates directory name
global_init(directory_name="my_templates")
```

In this example, the global_init function is called with the `directory_name` argument, so it will use the specified templates directory name instead of the default directory name "templates". The directory will be located in the same directory as the module where the `global_init` function is called.

## Customizing the Error Template

When the global_init function is called, it will look for a file called "error.html" in the templates directory. If this file does not exist, it will create a basic HTML page for it. This file is used as the default error template that is rendered when a Jinja2 template error occurs. The error template will receive a variable called FastJinja2TemplatesError with the error information, which you can use in the template to render the error message.

Here is an example of a sample Jinja2 error template that uses the FastJinja2TemplatesError variable to render the error message:

```
<!DOCTYPE html>
<html>
  <head>
    <title>Error</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/tailwindcss/dist/tailwind.min.css" />
  </head>
  <body>
    <div class="flex justify-center items-center h-screen">
      <h1>{{ FastJinja2TemplatesError }}</h1>
    </div>
  </body>
</html>
```

In this example, the error template uses the Tailwind CSS framework to center the error message on the screen. You can customize the error template as desired to match your application's styling and layout.

## Generating Dynamic Links within Jinja2 Templates

The template decorator function makes the `url_for` function from the FastAPI request object and the `URL` class from `starlette.datastructures.URL` available within Jinja2 templates.

To use these functions, you can simply call them in the template, like this:

```<a href="{{ url_for('route_name') }}">My Link</a>```
This will generate a link to the route named route_name using the url_for function.

To create URLs with query parameters using the URL class, you can use the include_query_params method, like this:

```{{ URL('route_name').include_query_params(query_param1="value1", query_param2="value2") }}```
This will create a URL to the route named route_name with the query parameters query_param1 and query_param2. You can then use these query parameters in your code as you would normally.

## Using Custom Functions in Jinja2 Templates

You can provide custom functions that can be used in the Jinja2 templates by passing the functions argument to the `global_init` function. This argument should be a dictionary of functions, where the keys are the function names and the values are the function objects. These functions will be added to the Jinja2 environment's globals dictionary, so they can be used in Jinja2 templates like any other global variable.

Here is an example of how to use the `global_init` function to add a custom function to the Jinja2 environment:

```
from fast_jinja2_templates import global_init

# Define a custom function
def my_function(value: str) -> str:
    return value.upper()

# Initialize the FastJinja2Templates instance and assign it to the templates global variable
# Pass the custom function to the Jinja2 environment
global_init(functions={"my_function": my_function})
```

In this example, the `global_init` function is called with the functions argument, so it will add the `my_function` function to the Jinja2 environment. This function can now be used in Jinja2 templates like any other global variable.

Here is an example of a Jinja2 template that uses the `my_function` custom function to render an uppercase version of the "`my_variable`" variable:

```
<!DOCTYPE html>
<html>
  <head>
    <title>My Template</title>
  </head>
  <body>
    <h1>{{ my_function(my_variable) }}</h1>
  </body>
</html>
```

In this example, the Jinja2 template uses the my_function function to convert the "my_variable" variable to uppercase and render it in an <h1> element. You can use custom functions in Jinja2 templates to perform custom operations on your template variables.

## Overriding the Default Template Path

By default, the template decorator function will use the "{module_name}/{function_name}.html" template path, where module_name is the name of the file where the FastAPI path operation function is defined and the function_name is the name of the decorated function. This means that the template for the index function in the previous example would be located at "main/index.html".

However, you can override this default behavior and specify a custom template path by passing the default template_name argument to the template decorator function when it is applied to a path operation function. This argument should be a string containing the path to the Jinja2 template that should be used for the path operation.

Here is an example of how to use the template decorator function to specify a custom template path:

```
from fastapi import FastAPI
from fast_jinja2_templates import template

app = FastAPI()

@app.get("/")
@template("my_custom_template.html")
def index(request: Request):
    return {"my_variable": "Hello, World!"}
```

In this example, the template decorator function is called with the specified custom template path instead of the default template path. The index function will now use the "my_custom_template.html" template (located in the root of the templates directory) instead of the "main/index.html" template.

You can use this feature to specify custom template paths for each path operation, allowing you to use different templates for different endpoints in your application.