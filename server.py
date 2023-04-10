
"""Server Requirements

The server should be able to:

Handle several clients connections
Transmit messages between clients

----------------------------------------------------

base from https://github.com/visheshdvivedi/Real-Time-Chat-Application"""

# Import required modules
import socket
import threading

HOST = '127.0.0.1'
PORT = 1234 # You can use any port between 0 to 65535
LISTENER_LIMIT = 5
active_clients = [] # List of all currently connected users

channel1 = [] # List of channel1 users
channel2 = [] # List of channel2 users

# Function to listen for upcoming messages from a client
def listen_for_messages(client, username):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message == '!exit':
            final_msg = "SERVER~" + username + ' disconnected'

            leave_channel1 = [i for i, v in enumerate(channel1) if v[0] == username]
            leave_channel2 = [i for i, v in enumerate(channel2) if v[0] == username]
            leave_channelactive = [i for i, v in enumerate(active_clients) if v[0] == username]
                
            if leave_channel1:
                channel1.pop(leave_channel1[0])

            if leave_channel2:
                channel2.pop(leave_channel2[0])

            if leave_channelactive:
                active_clients.pop(leave_channelactive[0])

            send_messages_to_all(final_msg)
            break
        if message != '':

            split_msg = message.split(",")

            channel = split_msg[0]
            msg = split_msg[1]
            
            final_msg = channel + '~' + username + "-> " + msg
            if channel == "chan1":
                search = [item for item in channel1 if username in item]
                leave_channel2 = [i for i, v in enumerate(channel2) if v[0] == username]
                
                if leave_channel2:
                    channel2.pop(leave_channel2[0])
                if not search:
                    channel1.append((username, client))
                send_messages_to_chan1(final_msg)
            elif channel == "chan2":
                search = [item for item in channel2 if username in item]
                leave_channel1 = [i for i, v in enumerate(channel1) if v[0] == username]

                if leave_channel1:
                    channel1.pop(leave_channel1[0])
                if not search:
                    channel2.append((username, client))
                send_messages_to_chan2(final_msg)
            else:
                search = [item for item in active_clients if channel in item]

                if search:
                    show_msg = "Private~" + "to " + search[0][0] + ": " + msg
                    client.sendall(show_msg.encode())

                    final_msg = "Private~" + username + "-> " + msg
                    send_message_to_client(search[0][1], final_msg)
                else:
                    final_msg = "SERVER~" + channel + ' is not on server'
                    client.sendall(final_msg.encode())
        else:
            print(f"The message send from client {username} is empty")



# Function to send message to a single client
def send_message_to_client(client, message):
    client.sendall(message.encode())

# Function to send any new message to all the clients that
# are currently connected to this server
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

def send_messages_to_chan1(message):
    for user in channel1:
        send_message_to_client(user[1], message)

def send_messages_to_chan2(message):
    for user in channel2:
        send_message_to_client(user[1], message)

def send_private_message(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

# Function to handle client
def client_handler(client):
    
    # Server will listen for client message that will
    # Contain the username
    while 1:

        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the server"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

# Main function
def main():

    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try catch block
    try:
        # Provide the server with an address in the form of
        # host IP and port
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    # Set server limit
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections
    while 1:

        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        Userthread = threading.Thread(target=client_handler, args=(client, ))
        Userthread.start()


if __name__ == '__main__':
    main()