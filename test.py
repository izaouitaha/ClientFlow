# IMPORT LIBRARIES

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import csv

#app settings

APP_TITLE = "Mini Client Follow-Up Tool"

DATA_FILE = "clients.json"

# create data file if it doesn`t exist.

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as file:
        json.dump([], file)

# this part is responsible for window.


root = tk.Tk()
root.title(APP_TITLE)
root.geometry("750x560")
root.resizable(True, True)
root.minsize(750, 560)


#  this part for title label


title_label = tk.Label(
    root,
    text="Mini Client Follow-Up Tool",
    font=("Arial", 20, "bold")
)

title_label.pack(pady=8)

####top form

form_frame = tk.Frame(root)
form_frame.pack(pady=10)

####this part for input clinet name 

name_label = tk.Label(form_frame, text="Client Name")
name_label.grid(row=0, column=0, padx=10)

name_entry = tk.Entry(form_frame, width=25)
name_entry.grid(row=1, column=0, padx=10)

####is for input  phone number


phone_label = tk.Label(form_frame, text="Phone Number")
phone_label.grid(row=0, column=1, padx=10)

phone_entry = tk.Entry(form_frame, width=25)
phone_entry.grid(row=1, column=1, padx=10)

####for input follow _up date

date_label = tk.Label(form_frame, text="Follow-Up Date")
date_label.grid(row=0, column=2, padx=10)

date_entry = tk.Entry(form_frame, width=25)
date_entry.grid(row=1, column=2, padx=10)

####seve new clint data

def save_client():

####get data from input fields

    client_name = name_entry.get()
    phone_number = phone_entry.get()
    followup_date = date_entry.get()

#### chek if any field is empty

    if client_name == "" or phone_number == "" or followup_date == "":
        messagebox.showwarning("Missing Data", "Please fill all fields")
        return
    
####create client data dictionary

    client_data = {
        "name": client_name,
        "phone": phone_number,
        "date": followup_date,
        "status": "Pending"
    }

    with open(DATA_FILE, "r") as file:
        clients = json.load(file)

    clients.append(client_data)

    with open(DATA_FILE, "w") as file:
        json.dump(clients, file, indent=4)

    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    client_table.insert(
        "",
        tk.END,
        values=(client_name, phone_number, followup_date, "Pending")
)

    messagebox.showinfo("Success", "Client saved successfully")

####save button

save_button = tk.Button(
    root,
    text="Save",
    width=10,
    height=1,
    command=save_client
)

save_button.pack(pady=8)

#### search input field

search_label = tk.Label(root, text="Search Client")
search_label.pack()

search_entry = tk.Entry(root, width=30)
search_entry.pack(pady=5)

search_entry.bind("<KeyRelease>", lambda event: search_clients())

####show client data in table

client_table = ttk.Treeview(
    root,
    columns=("Name", "Phone", "Date" ,"Status"),
    show="headings",
    height=6
)

client_table.heading("Name", text="Client Name")
client_table.heading("Phone", text="Phone Number")
client_table.heading("Date", text="Follow-Up Date")
client_table.heading("Status", text="Status")

client_table.pack(pady=10, fill="both", expand=True)

##### Show saved clients in the table

def load_clients():

    with open(DATA_FILE, "r") as file:
        clients = json.load(file)

    for client in clients:
        client_table.insert(
            "",
            tk.END,
            values=(client["name"], client["phone"], client["date"], client.get("status", "Pending"))
        )

load_clients()

#####search clients in the table based on name or phone number

def search_clients():
    search_text = search_entry.get().lower()

    for row in client_table.get_children():
        client_table.delete(row)

    with open(DATA_FILE, "r") as file:
        clients = json.load(file)

    for client in clients:
        if (
            search_text in client["name"].lower()
            or search_text in client["phone"]
        ):
            client_table.insert(
                "",
                tk.END,
                values=(
                    client["name"],
                    client["phone"],
                    client["date"],
                    client.get("status", "Pending")
                )
            )


####this is foer mark client as pending 


def mark_pending():
    selected_item = client_table.selection()

    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a client first")
        return

    client_table.item(
        selected_item,
        values=(
            client_table.item(selected_item)["values"][0],
            client_table.item(selected_item)["values"][1],
            client_table.item(selected_item)["values"][2],
            "Pending"
        )
    )

    with open(DATA_FILE, "r") as file:
        clients = json.load(file)

    selected_values = client_table.item(selected_item)["values"]

    for client in clients:

        if (
            client["name"] == selected_values[0]
            and client["phone"] == selected_values[1]
        ):
            client["status"] = "Pending"

    with open(DATA_FILE, "w") as file:
        json.dump(clients, file, indent=4)


##### this is for make client as contacted


def mark_contacted():
    selected_item = client_table.selection()

    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a client first")
        return

    client_table.item(
        selected_item,
        values=(
            client_table.item(selected_item)["values"][0],
            client_table.item(selected_item)["values"][1],
            client_table.item(selected_item)["values"][2],
            "Contacted"
        )
    )

    with open(DATA_FILE, "r") as file:
      clients = json.load(file)

    selected_values = client_table.item(selected_item)["values"]

    for client in clients:

     if (
        client["name"] == selected_values[0]
        and client["phone"] == selected_values[1]
    ):
        client["status"] = "Contacted"

    with open(DATA_FILE, "w") as file:
        json.dump(clients, file, indent=4)


 ##### is for delete client from table and data file 


def delete_client():
    selected_item = client_table.selection()

    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a client first")
        return

    selected_values = client_table.item(selected_item)["values"]

    with open(DATA_FILE, "r") as file:
        clients = json.load(file)

    updated_clients = []

    for client in clients:
        if not (
            client["name"] == selected_values[0]
            and client["phone"] == selected_values[1]
        ):
            updated_clients.append(client)

    with open(DATA_FILE, "w") as file:
        json.dump(updated_clients, file, indent=4)

    client_table.delete(selected_item)

    messagebox.showinfo("Deleted", "Client deleted successfully")


#### this is for export client data to csv file


def export_clients():
    with open(DATA_FILE, "r") as file:
        clients = json.load(file)

    if len(clients) == 0:
        messagebox.showwarning("No Data", "No clients to export")
        return

    with open("clients_export.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Name", "Phone", "Follow-Up Date", "Status"])

        for client in clients:
            writer.writerow([
                client["name"],
                client["phone"],
                client["date"],
                client.get("status", "Pending")
            ])

    messagebox.showinfo("Export Done", "Clients exported to clients_export.csv")


#### here you can find create buttons for mark as contacted, pending, delete and export data


####contacted button


button_frame = tk.Frame(root)
button_frame.pack(pady=10)

contacted_button = tk.Button(
    button_frame,
    text="Mark Contacted",
    width=20,
    height=1,
    command=mark_contacted
)

contacted_button.pack(side="left", padx=5)


####pending button


pending_button = tk.Button(
    button_frame,
    text="Mark Pending",
    width=20,
    height=1,
    command=mark_pending
)

pending_button.pack(side="left", padx=5)


#### delete button


delete_button = tk.Button(
    button_frame,
    text="Delete Client",
    width=20,
    height=1,
    command=delete_client
)

delete_button.pack(side="left", padx=5)


#### export button


export_button = tk.Button(
    button_frame,
    text="Export Excel",
    width=20,
    height=1,
    command=export_clients
)

export_button.pack(side="left", padx=5)



root.mainloop()

