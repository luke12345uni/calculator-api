from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

class CalculatorHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path != "/calculate":
            self.send_response(404)
            self.end_headers()
            return

        params = parse_qs(parsed.query)

        try:
            a = float(params["a"][0])
            b = float(params["b"][0])
            op = params["op"][0]
        except (KeyError, ValueError):
            self.send_response(400)
            self.end_headers()
            return

        result = self.calculate(a, b, op)

        response = {
            "a": a,
            "b": b,
            "operator": op,
            "result": result
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def calculate(self, a, b, op):
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        if op == "/":
            return None if b == 0 else a / b
        return None


def run():
    server = HTTPServer(("0.0.0.0", 8080), CalculatorHandler)
    print("Calculator server running on port 8080")
    server.serve_forever()


if __name__ == "__main__":
    run()
