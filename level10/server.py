#!/usr/bin/env python3
"""Simple multi-client TCP socket server listening on port 6969.

Each connected client is handled in its own thread. Whatever a client
sends is echoed back to it. Stop the server with Ctrl+C.
"""

import socket
import threading

HOST = "0.0.0.0"   # listen on all interfaces; use "127.0.0.1" for local only
PORT = 6969
BUFFER_SIZE = 1024


def handle_client(conn: socket.socket, addr: tuple) -> None:
    print(f"[+] Connected: {addr[0]}:{addr[1]}")
    with conn:
        conn.sendall(b"Welcome to the server! Type something and I'll echo it.\n")
        while True:
            try:
                data = conn.recv(BUFFER_SIZE)
            except ConnectionResetError:
                break
            if not data:  # client closed the connection
                break
            # Print everything received: byte count, raw bytes, and decoded text
            print(f"[{addr[0]}:{addr[1]}] {len(data)} bytes")
            print(f"  raw : {data!r}")
            print(f"  text: {data.decode('utf-8', errors='replace')}", end="", flush=True)
            if not data.endswith(b"\n"):
                print()
            conn.sendall(b"Echo: " + data)
    print(f"[-] Disconnected: {addr[0]}:{addr[1]}")


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # Allow quick restarts without "Address already in use" errors
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"[*] Server listening on {HOST}:{PORT}")

        try:
            while True:
                conn, addr = server.accept()
                thread = threading.Thread(
                    target=handle_client, args=(conn, addr), daemon=True
                )
                thread.start()
        except KeyboardInterrupt:
            print("\n[*] Shutting down server.")


if __name__ == "__main__":
    main()
