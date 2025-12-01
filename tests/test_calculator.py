from app.main import add, subtract, multiply, divide
import pytest

def test_add():
    assert add(20, 20) == 40

def test_add_fail():
    assert add(5, 5) == 10  # expected to pass

def test_subtract():
    assert subtract(10, 3) == 7

def test_multiply():
    assert multiply(6, 7) == 42

def test_divide():
    assert divide(8, 2) == 4

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
