class Calculator:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b

# Example usage:
if __name__ == "__main__":
    print(Calculator.add(5, 3))
    print(Calculator.subtract(10, 4))
    print(Calculator.multiply(6, 7))
    print(Calculator.divide(8, 2))