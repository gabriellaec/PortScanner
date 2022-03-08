import tkinter as tk
from tkinter import ttk, messagebox
import socket
import sys
from datetime import datetime
from queue import Queue
from threading import Thread, Lock


# ------------------------------------------------ #
# ----------- Configurando a interface ----------- #
# ------------------------------------------------ #
window = tk.Tk()
box_col=1


# title
title = tk.Label(
    text="Port Scanner",
    foreground="green", 
    background="#41c9f2",  
    font=("Arial", 20),
    width=10,
    height=2
)
title.grid(column=0, row=0)


# Host name
host = tk.Label(text="Host Name",
    foreground="black",  
    background="#41c9f2", 
    width=10,
    height=2
)
host_entry = tk.Entry()

host.grid(column=0, row=1)
host_entry.grid(column=box_col, row=1)


# Min range
range_min = tk.Label(text="Minimum Port Range",
    foreground="black",  
    background="#41c9f2",  
    width=15,
    height=2
)
input_range_min = tk.Entry()
range_min.grid(column=0, row=2)
input_range_min.grid(column=box_col, row=2)


# Max range
range_max = tk.Label(text="Maximum Port Range",
    foreground="black",  # Set the text color to white
    background="#41c9f2",  # Set the background color to black
    width=20,
    height=2
)
input_range_max = tk.Entry()
range_max.grid(column=0, row=3)
input_range_max.grid(column=box_col, row=3)


# Resultados
result_list = tk.Listbox(window,
    foreground="green",  
    background="black",  
    width=40,
    height=17,
    )
result_list.place (x=300,y=10)


# ------------------------------------------------ #
# ----------------- Port Scanner ----------------- #
# ------------------------------------------------ #
r_list = []
def scan_ports(port, host_name):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        sock.connect(((host_name), int(port)))                                         
        with Lock():    

            try:
                service = socket.getservbyport(port)
                text=f"Port {port} open | {service}"
            except:
                text=f"Port {port} open"                                       
            
            print(text)
            r_list.append(text)                                     
        sock.close()
    except (socket.timeout, ConnectionRefusedError): 
        pass

def threader(remoteServerIP):
    global queue
    while True:
        worker = queue.get()                                          
        scan_ports(worker, remoteServerIP)                                            
        queue.task_done()



# ----------------------------------------------------------------------- #
# ------------ Inicializando threads e mostrando resultados ------------- #
# ----------------------------------------------------------------------- #
threads = 100                                                           
queue = Queue()                                                         
socket.setdefaulttimeout(0.15)     

def start():
    
    # lendo valores dos textboxes
    host_name = host_entry.get()
    port_range_min = int(input_range_min.get())
    port_range_max = int(input_range_max.get())

    ports = [ p for p in range(port_range_min, port_range_max)]

    # checando se valores são válidos
    if host_name=="" or port_range_min=="" or port_range_min=="":
            messagebox.showinfo("Warning",  "Missing input!")


    # iniciando threads    
    remoteServerIP  = socket.gethostbyname(host_name)

    try:
        global queue
        for thread in range(threads):
            thread = Thread(target=threader, args=(remoteServerIP,))
            thread.daemon = True
            thread.start()                                                      

        for worker in ports:                                              
            queue.put(worker)

        queue.join()                                        


        print(sys.stdout)
        
    except KeyboardInterrupt:
        print ("Ctrl+C")
        sys.exit()


    
    status_label = tk.Label(
        window, text = f"Scanning host {remoteServerIP}",
        foreground="black",  
        background="#41c9f2",  
        width=20,
        height=3
    )
    status_label.grid(column=0, row=5)

    print(r_list)
    for i in range(0,len(r_list)):
        print(r_list[i])
        result_list.insert(i, r_list[i])

            

def clear():
    global r_list
    
    result_list.delete(0, tk.END)
    r_list=[]


start_button = tk.Button(window, text = "Start", command = start)
start_button.grid(column=1, row=4)


clear_button = tk.Button(window, text = "Clear", command = clear)
clear_button.grid(column=1, row=5)



# ------------------------------------------------ #
# ----------------- Renderizando ----------------- #
# ------------------------------------------------ #

ttk.Style().theme_use('vista')
window.configure(background="#41c9f2")
window.title('Port Scanner')
window.geometry("600x300+10+20")
window.mainloop()



# __________________________________________________________________________________________
# Referências:
# https://www.infinityloop.se/2020/08/23/how-to-make-a-multithreaded-port-scanner-in-python/
# https://www.geeksforgeeks.org/threaded-port-scanner-using-sockets-in-python/
# https://realpython.com/python-gui-tkinter/
# https://www.tutorialsteacher.com/python/create-gui-using-tkinter-python