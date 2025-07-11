import socket
import json
import base64
import logging

server_address = ("0.0.0.0", 7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received = ""  # empty string
        while True:
            # socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                # data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False


def remote_list():
    command_str = f"LIST"
    hasil = send_command(command_str)
    if hasil["status"] == "OK":
        print("daftar file : ")
        for nmfile in hasil["data"]:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False


def remote_get(filename=""):
    files = filename.split(" ")
    for nama_file in files:
        # command_str=f"GET {filename}"
        command_str = f"GET {nama_file}"
        hasil = send_command(command_str)
        if hasil["status"] == "OK":
            # proses file dalam bentuk base64 ke bentuk bytes
            namafile = hasil["data_namafile"]
            isifile = base64.b64decode(hasil["data_file"])
            fp = open(namafile, "wb+")
            fp.write(isifile)
            fp.close()
            # return True
        else:
            print("Gagal")
            return False
    return True


def remote_remove(filename=""):
    files = filename.split(" ")
    for nama_file in files:
        # command_str=f"GET {filename}"
        command_str = f"REMOVE {nama_file}"
        hasil = send_command(command_str)
        if hasil["status"] == "OK":
            print(f"file {nama_file} berhasil dihapus dari server")
        else:
            print("Gagal")
            return False
    return True


def remote_upload(filename=""):
    files = filename.split(" ")
    for nama_file in files:
        try:
            # membuka file lalu mengencode nya menjadi base64 byte
            with open(nama_file, "rb") as fp:
                file_content = base64.b64encode(fp.read()).decode()
            # mengirimkan string nama file dan isi nya melalui command_str
            command_str = f"UPLOAD {nama_file} {file_content}"
            # debug
            # print(file_content)
            hasil = send_command(command_str)
            if hasil["status"] == "OK":
                print(f"file {nama_file} berhasil diupload ke server")
            else:
                print("Gagal")
                return False
        except Exception as e:
            print(f"Gagal: {str(e)}")
            return False
    return True


if __name__ == "__main__":
    server_address = ("172.16.16.101", 9111)
    remote_list()
    remote_get("donalbebek.jpg pokijan.jpg")
    remote_remove("pokijan.jpg")
    remote_upload("langsat.jpg coba.txt")
