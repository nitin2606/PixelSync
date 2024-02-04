
import socket

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


