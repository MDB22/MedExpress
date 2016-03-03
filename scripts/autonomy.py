import dronekit
import socket
import exceptions

# Get IP address of vehicle
ip = raw_input("Enter IP address and port of desired vehicle: ")

if ip == "":
    ip = "tcp:127.0.0.1:5760"

# Connect to the Vehicle
print("Connecting to " + ip)

try:
    vehicle = dronekit.connect(ip, heartbeat_timeout=15, wait_ready=True)
# Bad TCP connection
except socket.error:
    print("No server exists!")
except dronekit.APIException:
    print("Timeout!")
# Bad TTY connection
except exceptions.OSError as e:
    print("No serial exists!")
# Other error
except:
    print("Something else went wrong!")

# About to exit script
vehicle.close()
