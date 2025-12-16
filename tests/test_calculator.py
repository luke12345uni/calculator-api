from app.main import CalculatorHandler
import pytest
import json
from unittest import mock
from http import HTTPStatus
import io

# --- Helper Class to Mock the Request Components ---

class MockSocketRequest:
    """A mock class that simulates the connection object passed to the Handler."""
    
    def __init__(self):
        # We need a BytesIO object for reading (rfile). Initialize it with nothing (b'').
        # When BaseHTTPRequestHandler calls readline(), this will immediately return b'', 
        # which correctly terminates the request reading loop without crashing.
        self.input_buffer = io.BytesIO(b'') 
        
        # We need a BytesIO object for output (wfile) to capture the response data.
        self.output_buffer = io.BytesIO()

    def makefile(self, mode, *args, **kwargs):
        """Simulate the creation of the request and response file objects."""
        if 'r' in mode:
            # Return the input buffer when BaseHTTPRequestHandler tries to read the request line
            return self.input_buffer
        if 'w' in mode:
            # Return the output buffer when BaseHTTPRequestHandler tries to write the response
            return self.output_buffer
        return mock.Mock() # Fallback

    def getsockname(self):
        """Mock the method that retrieves the client address."""
        return ('127.0.0.1', 8080)

# --- Pytest Fixture ---

@pytest.fixture
def handler():
    # Instantiate the handler with the mock request object
    request = MockSocketRequest()
    
    # Instantiate the handler. This works now because MockSocketRequest provides 
    # legitimate file-like objects (BytesIO) when the base class calls makefile().
    handler = CalculatorHandler(
        request=request, 
        client_address=('127.0.0.1', 12345), 
        server=mock.Mock()
    )

    # Manually map the internal request buffers to the handler attributes for assertion
    handler.rfile = request.input_buffer 
    handler.wfile = request.output_buffer 

    # Mock the response header/status methods we want to assert on
    handler.send_response = mock.Mock()
    handler.send_header = mock.Mock()
    handler.end_headers = mock.Mock()
    
    # This attribute must be set by the test before calling handler.do_GET()
    handler.path = "" 
    
    return handler

# --- Tests for the calculate method (Pure Function Test) ---

def test_calculate_add(handler):
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
    # Set the path/query
    handler.path = "/calculate?a=10&b=5&op=+"
    handler.do_GET()

    # 1. Check response code
    handler.send_response.assert_called_once_with(HTTPStatus.OK)
    
    # 2. Check headers
    handler.send_header.assert_called_with("Content-Type", "application/json")

    # 3. Check response body captured in the BytesIO buffer
    expected_response = {
        "a": 10.0,
        "b": 5.0,
        "operator": "+",
        "result": 15.0
    }
    handler.wfile.seek(0)
    written_data = handler.wfile.read()
    assert written_data == json.dumps(expected_response).encode()


def test_do_get_404_wrong_path(handler):
    handler.path = "/wrong_path"
    handler.do_GET()

    # 1
