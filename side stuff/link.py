import socket
import time

# RetroArch settings
RA_IP = "127.0.0.1"
RA_PORT = 55355

def send_command(command):
    """Sends a raw command string to RetroArch."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Commands must be strings like 'FAST_FORWARD' or 'GET_STATUS'
        sock.sendto(command.encode(), (RA_IP, RA_PORT))
        
        # Some commands (like GET_STATUS) return a response
        sock.settimeout(1.0)
        try:
            data, addr = sock.recvfrom(1024)
            return data.decode().strip()
        except socket.timeout:
            return None

# Examples of interaction:
# 1. Simulate Samus jumping (press 'A' for 0.1 seconds)
print("Jumping...")
send_command("BUTTON_DOWN;0;8") # 8 is typically the 'A' button index
time.sleep(0.1)
send_command("BUTTON_UP;0;8")

# 2. Get current game status (core name, content, etc.)
status = send_command("GET_STATUS")
print(f"Status: {status}")
# Read 2 bytes from Samus's health address
health_hex = send_command("READ_CORE_MEMORY 0x7E09A2 2")
if health_hex:
    # RetroArch returns hex strings; convert to integer
    health = int(health_hex.split()[1], 16)
    print(f"Current HP: {health}")
