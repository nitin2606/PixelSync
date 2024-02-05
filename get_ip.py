
import socket
import requests

def get_ip_address():
    try:
        # Create a socket connection to a remote server (here, Google's DNS server)
        # This will automatically determine the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except socket.error as e:
        print(f"Error: {e}")
        return None


def get_external_address():

    try:
        # Use httpbin to get the external IP address
        response = requests.get('https://httpbin.org/ip')
        ip_address = response.json()['origin']
        return ip_address
    except Exception as e:
        print(f"Error: {e}")
        return None