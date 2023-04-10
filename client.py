"""Client Requirements

The client should be able to:

set nickname
connect to the server by IP address
send text messages to other connected clients
Chat should support several channels
Chat should support private messages
Client should show messages from other clients
Client should be able to disconnect from the server

----------------------------------------------------

base from https://github.com/visheshdvivedi/Real-Time-Chat-Application"""


# import required modules
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import sys

HOST = '127.0.0.1'
PORT = 1234

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

# Creating a socket object
# AF_INET: we are going to use IPv4 addresses
# SOCK_STREAM: we are using TCP packets for communication
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():

    # try except block
    try:

        # Connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    thread = threading.Thread(target=listen_for_messages_from_server, args=(client, ))
    thread.daemon = True
    thread.start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    channel = channel_textbox.get()
    if (message != '' and channel != ''):
        final_message = channel + "," + message
        client.sendall(final_message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message or channel", "Message or channel cannot be empty")

def on_closing():
    try:
        message = "!exit"
        client.sendall(message.encode())
        client.shutdown(socket.SHUT_RDWR) #close the connection immediately
        client.close() #close the actual connection
    except:
        root.destroy() #close the window
    sys.exit()

root = tk.Tk()
root.geometry("600x600")
root.title("Messenger Client")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=4)
root.grid_rowconfigure(3, weight=1)
root.protocol("WM_DELETE_WINDOW", on_closing)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

channel_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
channel_frame.grid(row=1, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=2, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=3, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

channel_label = tk.Label(channel_frame, text="Enter channel:", font=FONT, bg=DARK_GREY, fg=WHITE)
channel_label.pack(side=tk.LEFT, padx=10)

channel_textbox = tk.Entry(channel_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
channel_textbox.pack(side=tk.LEFT)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


def listen_for_messages_from_server(client):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")
            
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")

# main function
def main():

    root.mainloop()
    
if __name__ == '__main__':
    main()