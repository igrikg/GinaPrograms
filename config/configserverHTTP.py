import http.server
import socketserver
import json
import pickle

# Set the directory you want to serve files from
directory = "."  # This serves files from the current directory

# Set the port you want to use
port = 30000

# Specify the JSON file to serve
json_file_path = "config.conf"

class JSONHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Read the JSON file and send its content
            with open(json_file_path, 'rb') as file:
                config_data = json.load(file)
                self.wfile.write(bytes(json.dumps(config_data), 'utf-8'))


try:
    # Create the server with the custom handler
    httpd = socketserver.TCPServer(("", port), JSONHandler)

    print(f"Serving on port {port}")
    httpd.serve_forever()

except KeyboardInterrupt:
    # Handle keyboard interrupt (e.g., Ctrl+C)
    print("\nClosing the server.")
    httpd.server_close()