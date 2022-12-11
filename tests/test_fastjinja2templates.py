import json
import os
import shutil
import tempfile
import pytest
from pathlib import Path

from fastapi import FastAPI
from fastapi import Request
from starlette.datastructures import URL
from starlette.testclient import TestClient

from fastjinja2templates import FastJinja2Templates, global_init, template

# Test the FastJinja2Templates class
def test_FastJinja2Templates():
    # Create a temporary directory for the test
    with tempfile.TemporaryDirectory() as tempdir:
        # Create a FastJinja2Templates instance with a nonexistent directory
        with pytest.raises(FastJinja2Templates.TemplatesDirectoryNotFound):
            FastJinja2Templates(directory_name="nonexistent")

        # Create a FastJinja2Templates instance with a valid directory
        templates = FastJinja2Templates(directory_name=tempdir)

        # Verify that the templates directory was set correctly
        # assert templates.env.globalsdirectory == tempdir

        # Verify that the global functions were added correctly
        assert "URL" in templates.env.globals
        assert templates.env.globals["URL"] == URL

# Test the global_init function
def test_global_init():
    # Create a temporary directory for the test
    with tempfile.TemporaryDirectory() as tempdir:
        # Initialize the global templates variable
        templates = global_init(directory_name=tempdir)

        # Verify that the searchpath of the Jinja File system loader matches the temporary directory
        assert templates.env.loader.searchpath == [tempdir]

        # Verify that the global functions were added correctly
        assert "URL" in templates.env.globals
        assert templates.env.globals["URL"] == URL

# Test the template decorator
def test_template_decorator_custom_directory_path():
    # Create a temporary directory called "templates"
    with tempfile.TemporaryDirectory() as tempdir:
        # Create an empty HTML file called 'home.html' within the temporary directory
        with open(os.path.join(tempdir, "home.html"), "w") as f:
            f.write("{{ message }}")

        # Create a test FastAPI app
        app = FastAPI()
        global_init(directory=tempdir)

        # Define a synchronous route that uses the template decorator
        @app.get("/")
        @template("home.html")
        def home(request: Request):
            return {"message": "Hello, world!"}

        # Define an asynchronous route that uses the template decorator
        @app.get("/async")
        @template("home.html")
        async def home_async(request: Request):
            return {"message": "Hello, world!"}

        # Create a test client
        client = TestClient(app)

        # Send a request to the synchronous route and verify that the response is correct
        response = client.get("/")
        assert response.status_code == 200

        # Verify that the response contains the "message" passed by the "home" endpoint
        assert "Hello, world!" in response.text

        # Send a request to the asynchronous route and verify that the response is correct
        response = client.get("/async")
        assert response.status_code == 200

        # Verify that the response contains the "message" passed by the "home_async" endpoint
        assert "Hello, world!" in response.text

# Test the template decorator
def test_template_decorator_default_init():
    # Create a temporary directory in the current working directory
    tempdir_path = os.path.join(os.getcwd(),"fastjinja2templates","templates") 
    #tempfile.mkdtemp(dir=os.path.join(os.getcwd(),"fastjinja2templates","templates"), name="templates")
    os.mkdir(tempdir_path)
    # Create an empty HTML file called 'home.html' within the temporary directory
    with open(os.path.join(tempdir_path, "home.html"), "w") as f:
        f.write("{{ message }}")

    # Initialize the global templates variable without any parameters
    global_init()

    # Create a test FastAPI app
    app = FastAPI()

    # Define a synchronous route that uses the template decorator
    @app.get("/")
    @template("home.html")
    def home(request: Request):
        return {"message": "Hello, world!"}

    # Define an asynchronous route that uses the template decorator
    @app.get("/async")
    @template("home.html")
    async def home_async(request: Request):
        return {"message": "Hello, world!"}

    # Create a test client
    client = TestClient(app)

    # Send a request to the synchronous route and verify that the response is correct
    response = client.get("/")
    assert response.status_code == 200

    # Verify that the response contains the "message" passed by the "home" endpoint
    assert "Hello, world!" in response.text

    # Send a request to the asynchronous route and verify that the response is correct
    response = client.get("/async")
    assert response.status_code == 200

    # Verify that the response contains the "message" passed by the "home_async" endpoint
    assert "Hello, world!" in response.text

    # Check if the directory exists
    if os.path.exists(tempdir_path):
        # If the directory exists, remove it and all of its contents
        shutil.rmtree(tempdir_path)

def test_template_not_found():
    # Create a test FastAPI app
    app = FastAPI()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Initialize the FastJinja2Templates object with the error template string
        global_init(directory=temp_dir)

        # Define a test route with the template decorator
        assert os.path.exists(temp_dir)
        assert os.path.exists(os.path.join(temp_dir,"test.html")) == False

        @app.get("/")
        @template("test.html")
        def test_route(request: Request):
            return {"message": "Hello, world!"}

        # Define a test client for the app
        with TestClient(app) as client:
            # Send a request to the test route
            response = client.get("/")

            # Check that the response status code is 500
            assert response.status_code == 500

            # Check that the response body contains the expected error message
            assert "Template not found" in response.text
            assert "test.html" in response.text
            assert "Hello, world!" not in response.text