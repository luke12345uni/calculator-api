from app.main import CalculatorHandler
import pytest
import json
from unittest import mock
from http import HTTPStatus
import io # Although not explicitly used, good practice to import for I/O simulation

# --- Fixtures ---

@pytest.fixture
def handler():
    # The fix: Patch BaseHTTPRequestHandler.__init__ to prevent it from immediately
    # calling self.handle() and attempting to read the socket, which fails with mocks.
    with mock.patch('http.server.BaseHTTPRequestHandler.__init__'):
        # Instantiate the handler (actual init is skipped by the patch)
        handler = CalculatorHandler(
            request=mock.Mock(), 
            client_address=('127.0.0.1', 12345), 
            server=mock.Mock()
        )

    # Manually set the required mock attributes that BaseHTTPRequestHandler normally sets
    # and that the tests rely on.
    handler.rfile = mock.Mock() # Mock the input file stream
    handler.wfile = mock.Mock() # Mock the output file stream for writing the response body
    handler.send_response = mock.Mock()
    handler.send_header = mock.Mock()
    handler.end_headers = mock.Mock()
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
    # The calculate method returns None on division by zero
    assert handler.calculate(10, 0, "/") is None

def test_calculate_invalid_op(handler):
    # The calculate method returns None for an unknown operator
    assert handler.calculate(10, 5, "**") is None

# --- Tests for the do_GET method (HTTP Handler Test) ---

def test_do_get_success_add(handler):
    # Simulate the request path/query
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
    # Check the call to the mocked wfile.write (response body as bytes)
    handler.wfile.write.assert_called_once_with(json.dumps(expected_response).encode())


def test_do_get_404_wrong_path(handler):
    handler.path = "/wrong_path"
    handler.do_GET()

    # 1. Check response code
    handler.send_response.assert_called_once_with(HTTPStatus.NOT_FOUND)
    
    # 2. Check that the main logic (wfile.write) was NOT called
    handler.wfile.write.assert_not_called()
    handler.end_headers.assert_called_once()

def test_do_get_400_missing_param(handler):
    # Missing 'b' parameter
    handler.path = "/calculate?a=10&op=+"
    handler.do_GET()

    # Check response code
    handler.send_response.assert_called_once_with(HTTPStatus.BAD_REQUEST)
    handler.wfile.write.assert_not_called()
    handler.end_headers.assert_called_once()

def test_do_get_400_invalid_number_param(handler):
    # 'a' is not a valid float
    handler.path = "/calculate?a=ten&b=5&op=+"
    handler.do_GET()

    # Check response code
    handler.send_response.assert_called_once_with(HTTPStatus.BAD_REQUEST)
    handler.wfile.write.assert_not_called()
    handler.end_headers.assert_called_once()

def test_do_get_200_divide_by_zero_result_none(handler):
    handler.path = "/calculate?a=10&b=0&op=/"
    handler.do_GET()

    # 1. Check response code (still 200, as the server handled the request gracefully)
    handler.send_response.assert_called_once_with(HTTPStatus.OK)

    # 2. Check response body for "result": None
    expected_response = {
        "a": 10.0,
        "b": 0.0,
        "operator": "/",
        "result": None 
    }
    handler.wfile.write.assert_called_once_with(json.dumps(expected_response).encode())
