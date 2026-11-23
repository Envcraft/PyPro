"""CLI Calculator — implement your solution here."""


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


def modulus(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Modulus by zero is not allowed.")
    return a % b


def power(a: float, b: float) -> float:
    return a ** b


def calculate(a: float, operator: str, b: float) -> float:
    ops = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
        "%": modulus,
        "**": power,
    }
    if operator not in ops:
        raise ValueError(f"Unknown operator '{operator}'. Use: {', '.join(ops)}")
    return ops[operator](a, b)


def get_number(prompt: str) -> float | None:
    try:
        return float(input(prompt))
    except ValueError:
        print("Error: Please enter a valid number.")
        return None


def main() -> None:
    print("CLI Calculator  |  operators: + - * / % **  |  type 'quit' or 'exit' to stop\n")
    while True:
        a = get_number("Enter first number: ")
        if a is None:
            continue

        operator = input("Enter operator (+, -, *, /, %, **): ").strip()
        if operator.lower() in ("quit", "exit"):
            break

        b = get_number("Enter second number: ")
        if b is None:
            continue

        try:
            result = calculate(a, operator, b)
            print(f"Result: {a} {operator} {b} = {result}\n")
        except ValueError as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
