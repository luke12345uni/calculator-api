import time

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b

def main():
    print("Simple Calculator")
    print("-----------------")
    print("Choose operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")
    
    # Original line causing the error
    # choice = input("Enter choice (1-5): ")

    # Replace input() with a fixed value for automation
    choice = "1"  # This is a predefined choice (could also be passed as an environment variable)
    
    time.sleep(120)
    if choice == "1":
        # Perform addition
        print("Addition selected.")
        result = add(5, 3)
        print(f"Result: {result}")

    elif choice == "2":
        # Perform subtraction
        pass
    elif choice == "3":
        # Perform multiplication
        pass
    elif choice == "4":
        # Perform division
        pass
    elif choice == "5":
        # Exit
        pass


if __name__ == "__main__":
    main()
