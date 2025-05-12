import serial
import time

# Define the UART port and configuration (adjust as needed)
uart_port = "/dev/ttyUSB0"  # Change this to your correct port (Windows: 'COMx', Linux: '/dev/ttyUSBx')
baud_rate = 9600  # Baud rate, ensure it matches the device's setting
timeout = 1  # Timeout for reading data in seconds

# Open the serial port
ser = serial.Serial(uart_port, baudrate=baud_rate, timeout=timeout)


# Function to send a command over UART
def send_command(command):
    if ser.is_open:
        ser.write(command.encode())  # Send the command (needs to be bytes)
        print(f"Sent: {command}")
    else:
        print("Serial port is not open!")


# Function to read data from UART
def read_data():
    if ser.is_open:
        data = ser.readline()  # Reads a full line from the UART interface
        if data:
            return data.decode().strip()  # Decode bytes to string and strip any extra whitespace
        else:
            return None
    else:
        print("Serial port is not open!")
        return None


# Main loop to continuously read commands from UART and echo back
try:
    while True:
        print("Waiting for command...")

        # Read incoming data
        received = read_data()
        if received:
            print(f"Received: {received}")
            # Echo back the received data (or process it as needed)
            send_command(f"Echo: {received}\n")

        # Add a small delay to avoid overloading the CPU
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    # Clean up and close the UART connection
    if ser.is_open:
        ser.close()
        print("Closed the serial port.")
