from app.main import CalculatorHandler
import pytest
import json
from unittest import mock
from http import HTTPStatus

# --- Fixtures ---

# A fixture to provide a mocked CalculatorHandler instance for each test
@pytest.fixture
def handler():
    # Mock the required BaseHTTPRequestHandler attributes
    # wfile.write is what sends the actual response data
    handler = CalculatorHandler(
        request=mock.Mock(), # A mock for the socket request
        client_address=('127.0.0.1', 12345), # A dummy address
        server=mock.Mock() # A mock for the server instance
    )
    # Mock methods that BaseHTTPRequestHandler calls to send the response
    handler.send_response = mock.Mock()
    handler.send_header = mock.Mock()
    handler.end_headers = mock.Mock()
    handler.wfile = mock.Mock()
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
    # Set the path that the handler will parse
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
    # The response is written to wfile as bytes, so we check the mock call arguments
    handler.wfile.write.assert_called_once_with(json.dumps(expected_response).encode())


def test_do_get_404_wrong_path(handler):
    handler.path = "/wrong_path"
    handler.do_GET()

    # 1. Check response code
    handler.send_response.assert_called_once_with(HTTPStatus.NOT_FOUND)
    
    # 2. Check that the main logic (wfile.write) was NOT called
    handler.wfile.write.assert_not_called()
    # end_headers is called after send_response for 404
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

    # 1. Check response code (still 200, as the server handles the operation, but the result is None)
    handler.send_response.assert_called_once_with(HTTPStatus.OK)

    # 2. Check response body for "result": None
    expected_response = {
        "a": 10.0,
        "b": 0.0,
        "operator": "/",
        "result": None # The handler's calculate method returns None here
    }
    handler.wfile.write.assert_called_once_with(json.dumps(expected_response).encode())
