from app.main import CalculatorHandler
import pytest
import json
from unittest import mock
from http import HTTPStatus
import io

# --- Helper Class to Mock the Request Components ---

class MockSocketRequest:
    """A minimal mock class that simulates the connection object passed to the Handler."""
    
    # We provide a mock file-like object for input (rfile) that can be read.
    # We just need to mock the minimum necessary to instantiate the handler.
    rfile = io.BytesIO(b'') # A mock stream for reading the request
    
    # We need a BytesIO object for output (wfile) to capture the response data.
    wfile = io.BytesIO()

    def makefile(self, *args, **kwargs):
        """Mock the makefile method that BaseHTTPRequestHandler uses."""
        # This implementation is often sufficient, but for robust mocking, 
        # we often use BytesIO objects directly or mocks that have a read/write interface.
        return mock.Mock() 

    def getsockname(self):
        return ('127.0.0.1', 8080)

# --- CORRECTED Fixture ---

@pytest.fixture
def handler():
    # Instantiate the handler with the minimal necessary mock objects.
    # The MockSocketRequest class provides the rfile and wfile objects that BaseHTTPRequestHandler
    # needs to initialize without crashing.

    request = MockSocketRequest()
    
    # Instantiate the handler normally. Since MockSocketRequest provides the I/O streams, 
    # the base class's __init__ will not immediately crash.
    handler = CalculatorHandler(
        request=request, 
        client_address=('127.0.0.1', 12345), 
        server=mock.Mock()
    )

    # Now, mock the methods that handle sending the *response* headers/status.
    # We do NOT mock rfile/wfile here, as they are provided by MockSocketRequest.
    handler.send_response = mock.Mock()
    handler.send_header = mock.Mock()
    handler.end_headers = mock.Mock()
    
    # We keep the wfile from the MockSocketRequest object, as it captures the response data.
    handler.wfile = request.wfile 
    handler.path = "" # Path will be set by each test before calling do_GET
    
    return handler

# --- Tests for the calculate method (Pure Function Test) ---

def test_calculate_add(handler):
    # Test the internal calculate logic
    assert handler.calculate(5, 5, "+") == 10
    assert handler.calculate(10.5, 2.5, "+") == 13.0

def test_calculate_subtract(handler):
    assert handler.calculate(10, 3, "-") == 7

def test_calculate_multiply(handler):
    assert handler.calculate(6, 7, "*") == 42

def test_calculate_divide(handler):
    assert handler.calculate(8, 2, "/") == 4.0
    assert handler.calculate(10, 4, "/") == 2.5

def test_calculate_divide_by_zero(handler):
    assert handler.calculate(10, 0, "/") is None

def test_calculate_invalid_op(handler):
    assert handler.calculate(10, 5, "**") is None

# --- Tests for the do_GET method (HTTP Handler Test) ---

def test_do_get_success_add(handler):
    handler.path = "/calculate?a=10&b=5&op=+"
    handler.do_GET()

    # 1. Check response code
    handler.send_response.assert_called_once_with(HTTPStatus.OK)
    
    # 2. Check headers
    handler.send_header.assert_called_with("Content-Type", "application/json")

    # 3. Check response body
    expected_response = {
        "a": 10.0,
        "b": 5.0,
        "operator": "+",
        "result": 15.0
    }
    # Check the data captured in the BytesIO object
    handler.wfile.seek(0)
    written_data = handler.wfile.read()
    
    # Since wfile.write is not mocked, we check the content of the stream.
    # The output is compared to the expected JSON, encoded to bytes.
    assert written_data == json.dumps(expected_response).encode()


def test_do_get_404_wrong_path(handler):
    handler.path = "/wrong_path"
    handler.do_GET()

    # 1. Check response code
    handler.send_response.assert_called_once_with(HTTPStatus.NOT_FOUND)
    
    # 2. Check that no body data was written
    handler.wfile.seek(0)
    assert handler.wfile.read() == b''
    handler.end_headers.assert_called_once()


def test_do_get_400_missing_param(handler):
    handler.path = "/calculate?a=10&op=+"
    handler.do_GET()

    # Check response code
    handler.send_response.assert_called_once_with(HTTPStatus.BAD_REQUEST)
    handler.wfile.seek(0)
    assert handler.wfile.read() == b''
    handler.end_headers.assert_called_once()

def test_do_get_400_invalid_number_param(handler):
    handler.path = "/calculate?a=ten&b=5&op=+"
    handler.do_GET()

    # Check response code
    handler.send_response.assert_called_once_with(HTTPStatus.BAD_REQUEST)
    handler.wfile.seek(0)
    assert handler.wfile.read() == b''
    handler.end_headers.assert_called_once()

def test_do_get_200_divide_by_zero_result_none(handler):
    handler.path = "/calculate?a=10&b=0&op=/"
    handler.do_GET()

    # 1. Check response code 
    handler.send_response.assert_called_once_with(HTTPStatus.OK)

    # 2. Check response body for "result": None
    expected_response = {
        "a": 10.0,
        "b": 0.0,
        "operator": "/",
        "result": None 
    }
    handler.wfile.seek(0)
    written_data = handler.wfile.read()
    assert written_data == json.dumps(expected_response).encode()
