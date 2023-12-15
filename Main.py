import sqlite3
import tkinter as tk
from tkinter import simpledialog


# Function to create a connection to the SQLite database
def create_connection(database):
    try:
        connection = sqlite3.connect(database)
        return connection
    except sqlite3.Error as e:
        print(e)
    return None


# Function to add a new contact to the database
def add_contact(connection, nom, prenom, jour, mois, annee, address_email, numero_telephone, numero_et_rue, ville,
                code_postal):
    try:
        cursor = connection.cursor()

        # Insert date of birth into DateOfBirth table
        cursor.execute("INSERT INTO DateDeNaissance (Jour, Mois, Annee) VALUES (?, ?, ?)", (jour, mois, annee))
        date_of_birth_id = cursor.lastrowid

        # Insert address into Address table
        cursor.execute("INSERT INTO Address (NumeroEtRue, Ville, CodePostal) VALUES (?, ?, ?)",
                       (numero_et_rue, ville, code_postal))
        address_id = cursor.lastrowid

        # Insert contact into Contact table with foreign keys
        cursor.execute("""
            INSERT INTO Contact (Nom, Prenom, DateDeNaissance_ID, AddressEmail, NumeroDeTelephone, Address_ID)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nom, prenom, date_of_birth_id, address_email, numero_telephone, address_id))

        connection.commit()
        print("Contact added successfully!")

    except sqlite3.Error as e:
        connection.rollback()
        print("Error adding contact:", e)

    finally:
        cursor.close()


# Function to add a new contact using Tkinter with a single form window
def add_contact_from_user_input(connection):
    # Create a Tkinter window for user input
    root = tk.Tk()
    root.title("Add New Contact")
    root.geometry("400x400")

    # Create a frame for the form
    form_frame = tk.Frame(root)
    form_frame.pack(expand=tk.YES, fill=tk.BOTH)

    # Create a canvas for the form with a scrollbar
    canvas = tk.Canvas(form_frame)
    scrollbar = tk.Scrollbar(form_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the form
    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor=tk.CENTER)

    # Entry variables
    entry_vars = [tk.StringVar() for _ in range(10)]

    # Function to get values and add contact
    def submit():
        nom = entry_widgets[0].get()
        prenom = entry_widgets[1].get()
        jour = entry_widgets[2].get()
        mois = entry_widgets[3].get()
        annee = entry_widgets[4].get()
        address_email = entry_widgets[5].get()
        numero_telephone = entry_widgets[6].get()
        numero_et_rue = entry_widgets[7].get()
        ville = entry_widgets[8].get()
        code_postal = entry_widgets[9].get()

        # Check if any field is empty
        if any(value == "" for value in
               [nom, prenom, jour, mois, annee, address_email, numero_telephone, numero_et_rue, ville, code_postal]):
            print("Please fill in all the fields.")
        else:
            add_contact(connection, nom, prenom, jour, mois, annee, address_email, numero_telephone, numero_et_rue,
                        ville, code_postal)
            root.destroy()

    # Function to close the window without adding a new contact
    def cancel():
        root.destroy()

    # Form labels and entry widgets
    labels = ["Last Name:", "First Name:", "Day of Birth:", "Month of Birth:", "Year of Birth:", "Email Address:",
              "Phone Number:", "Street Address:", "City:", "Postal Code:"]

    entry_widgets = []

    for label, var in zip(labels, entry_vars):
        label_widget = tk.Label(inner_frame, text=label)
        entry_widget = tk.Entry(inner_frame, textvariable=var)

        label_widget.pack(anchor=tk.CENTER, side=tk.TOP, pady=5)
        entry_widget.pack(anchor=tk.CENTER, side=tk.TOP, pady=5)

        entry_widgets.append(entry_widget)

    # Submit and Cancel buttons
    button_frame = tk.Frame(inner_frame)
    button_frame.pack(side=tk.TOP, pady=10)

    tk.Button(button_frame, text="Submit", command=submit).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Cancel", command=cancel).pack(side=tk.LEFT, padx=10)

    # Configure the canvas to scroll the inner frame
    inner_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    root.mainloop()


# Function to display detailed information for a contact
def show_contact_info(connection, contact):
    def open_modify_page():
        root.destroy()
        modify_contact_info(connection, contact)

    def delete_contact():
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Contact WHERE Nom=? AND Prenom=?", (contact[0], contact[1]))
        connection.commit()
        cursor.close()
        root.destroy()

    # Create a new Tkinter window for detailed information
    root = tk.Tk()
    root.title("Contact Information")
    root.geometry("400x450")

    # Fetch detailed information from the database based on the contact
    cursor = connection.cursor()
    cursor.execute("""
        SELECT Nom, Prenom, DateDeNaissance.Jour, DateDeNaissance.Mois, DateDeNaissance.Annee,
               AddressEmail, NumeroDeTelephone, Address.NumeroEtRue, Address.Ville, Address.CodePostal
        FROM Contact
        JOIN DateDeNaissance ON Contact.DateDeNaissance_ID = DateDeNaissance.DateDeNaissance_ID
        JOIN Address ON Contact.Address_ID = Address.Address_ID
        WHERE Nom=? AND Prenom=?
    """, (contact[0], contact[1]))

    contact_info = cursor.fetchone()

    # Create a canvas for the contact information with a scrollbar
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the contact information
    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor=tk.NW)

    # Display detailed information
    labels = ["Last Name:", "First Name:", "Day of Birth:", "Month of Birth:", "Year of Birth:", "Email Address:",
              "Phone Number:", "Street Address:", "City:", "Postal Code:"]

    for label, value in zip(labels, contact_info):
        tk.Label(inner_frame, text=label).pack(anchor=tk.W)
        tk.Label(inner_frame, text=value).pack(anchor=tk.W)

    # Buttons for Modify and Delete
    button_frame = tk.Frame(inner_frame)
    button_frame.pack(side=tk.TOP, pady=10)

    tk.Button(button_frame, text="Modify", command=open_modify_page).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Delete", command=delete_contact).pack(side=tk.LEFT, padx=10)

    # Configure the canvas to scroll the inner frame
    inner_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    root.mainloop()


# Function to modify contact information
def modify_contact_info(connection, contact):
    # Create a new Tkinter window for choosing what to modify
    choose_modify_type_window = tk.Tk()
    choose_modify_type_window.title("Choose Modification Type")
    choose_modify_type_window.geometry("300x300")

    # Create a listbox to display modification types
    modify_types = ["First Name", "Last Name", "Date of Birth", "Email Address", "Phone Number", "Street Address",
                    "City", "Postal Code"]

    modify_types_listbox = tk.Listbox(choose_modify_type_window, selectmode=tk.SINGLE)
    modify_types_listbox.pack(expand=tk.YES, fill=tk.BOTH)

    for modify_type in modify_types:
        modify_types_listbox.insert(tk.END, modify_type)

    # Function to handle scrolling with arrow keys for modification types
    def on_modify_type_arrow_key(event):
        selected_index = modify_types_listbox.curselection()
        if event.keysym == 'Up':
            if selected_index:
                modify_types_listbox.selection_clear(selected_index[0])
                modify_types_listbox.selection_set(selected_index[0] - 1)
        elif event.keysym == 'Down':
            if selected_index:
                modify_types_listbox.selection_clear(selected_index[0])
                modify_types_listbox.selection_set(selected_index[0] + 1)
        elif event.keysym == 'Return':
            open_modify_input_page()

    # Bind the arrow keys to the listbox for scrolling
    modify_types_listbox.bind("<Up>", on_modify_type_arrow_key)
    modify_types_listbox.bind("<Down>", on_modify_type_arrow_key)
    modify_types_listbox.bind("<Return>", on_modify_type_arrow_key)

    # Function to open the modification input page
    def open_modify_input_page():
        selected_index = modify_types_listbox.curselection()
        if selected_index:
            selected_modify_type = modify_types[selected_index[0]]
            choose_modify_type_window.destroy()
            modify_input_window = tk.Toplevel()
            modify_input_window.title("Enter New Value")
            modify_input_window.geometry("400x200")

            # Entry variable
            entry_var = tk.StringVar()

            # Create a frame for the input form
            form_frame = tk.Frame(modify_input_window)
            form_frame.pack(expand=tk.YES, fill=tk.BOTH)

            # Label and entry widget
            tk.Label(form_frame, text=f"Enter new {selected_modify_type} for {contact[0]} {contact[1]}:").pack(
                anchor=tk.W)
            entry_widget = tk.Entry(form_frame, textvariable=entry_var)
            entry_widget.pack(anchor=tk.W, pady=10)

            # Function to submit the modification
            def submit():
                new_value = entry_var.get()
                if new_value:
                    update_contact_field(connection, contact, selected_modify_type, new_value)
                    modify_input_window.destroy()
                    modify_contact_info(connection, contact)
                else:
                    print("Please enter a new value.")

            def return_page():
                modify_input_window.destroy()
                modify_contact_info(connection, contact)

            # Submit button
            tk.Button(form_frame, text="Submit", command=submit).pack(side=tk.LEFT, padx=10)
            tk.Button(form_frame, text="Return", command=return_page).pack(side=tk.LEFT, padx=10)

            modify_input_window.mainloop()

    # Bind the function to open the modification input page
    choose_modify_type_window.bind("<Return>", lambda event: on_modify_type_arrow_key(event))

    # Enter the Tkinter event loop for choosing modification type
    choose_modify_type_window.mainloop()


# Function to update contact field based on modification type
def update_contact_field(connection, contact, modify_type, new_value):
    cursor = connection.cursor()
    if modify_type == "First Name":
        cursor.execute("UPDATE Contact SET Prenom=? WHERE Nom=? AND Prenom=?", (new_value, contact[0], contact[1]))
    elif modify_type == "Last Name":
        cursor.execute("UPDATE Contact SET Nom=? WHERE Nom=? AND Prenom=?", (new_value, contact[0], contact[1]))
    elif modify_type == "Date of Birth":
        # Assuming the date of birth is in the format "Day Month Year"
        day, month, year = new_value.split()
        cursor.execute("""
            UPDATE DateDeNaissance
            SET Jour=?, Mois=?, Annee=?
            WHERE DateDeNaissance_ID=(
                SELECT DateDeNaissance_ID FROM Contact
                WHERE Nom=? AND Prenom=?
            )
        """, (day, month, year, contact[0], contact[1]))
    elif modify_type == "Email Address":
        cursor.execute("UPDATE Contact SET AddressEmail=? WHERE Nom=? AND Prenom=?",
                       (new_value, contact[0], contact[1]))
    elif modify_type == "Phone Number":
        cursor.execute("UPDATE Contact SET NumeroDeTelephone=? WHERE Nom=? AND Prenom=?",
                       (new_value, contact[0], contact[1]))
    elif modify_type == "Street Address":
        cursor.execute("""
            UPDATE Address
            SET NumeroEtRue=?
            WHERE Address_ID=(
                SELECT Address_ID FROM Contact
                WHERE Nom=? AND Prenom=?
            )
        """, (new_value, contact[0], contact[1]))
    elif modify_type == "City":
        cursor.execute("""
            UPDATE Address
            SET Ville=?
            WHERE Address_ID=(
                SELECT Address_ID FROM Contact
                WHERE Nom=? AND Prenom=?
            )
        """, (new_value, contact[0], contact[1]))
    elif modify_type == "Postal Code":
        cursor.execute("""
            UPDATE Address
            SET CodePostal=?
            WHERE Address_ID=(
                SELECT Address_ID FROM Contact
                WHERE Nom=? AND Prenom=?
            )
        """, (new_value, contact[0], contact[1]))

    connection.commit()
    cursor.close()


# Function to display contacts and allow selecting with arrow keys
def display_contacts(connection):
    # Create a Tkinter window for displaying contacts
    contacts_window = tk.Toplevel()
    contacts_window.title("Contacts")
    contacts_window.geometry("400x400")

    # Create a search bar
    search_var = tk.StringVar()
    search_entry = tk.Entry(contacts_window, textvariable=search_var)
    search_entry.pack(pady=10)

    # Create a listbox to display contacts
    contacts_listbox = tk.Listbox(contacts_window, selectmode=tk.SINGLE)
    contacts_listbox.pack(expand=tk.YES, fill=tk.BOTH)

    # Fetch contacts from the database
    cursor = connection.cursor()
    cursor.execute("SELECT Nom, Prenom, AddressEmail FROM Contact")
    contacts = cursor.fetchall()

    for contact in contacts:
        contacts_listbox.insert(tk.END, f"{contact[0]} {contact[1]} - {contact[2]}")

    cursor.close()

    # Function to open detailed information when Return key is pressed
    def open_contact_info(event):
        selected_index = contacts_listbox.curselection()
        if selected_index:
            selected_contact = contacts[selected_index[0]]
            show_contact_info(connection, selected_contact)

    # Bind the function to open contact info when Return key is pressed
    contacts_listbox.bind("<Return>", open_contact_info)

    # Function to update the list of contacts based on the search
    def update_contacts_list(event):
        search_term = search_var.get().lower()
        contacts_listbox.delete(0, tk.END)

        # Fetch contacts from the database based on the search term
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Nom, Prenom, AddressEmail
            FROM Contact
            WHERE LOWER(Nom) LIKE ? OR LOWER(Prenom) LIKE ? OR LOWER(AddressEmail) LIKE ?
        """, ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))

        nonlocal contacts  # Use nonlocal instead of global
        contacts = cursor.fetchall()

        for contact in contacts:
            contacts_listbox.insert(tk.END, f"{contact[0]} {contact[1]} - {contact[2]}")

        cursor.close()

    # Bind the update function to the search entry
    search_entry.bind("<KeyRelease>", update_contacts_list)

    # Function to handle scrolling with arrow keys
    def on_arrow_key(event):
        selected_index = contacts_listbox.curselection()
        if event.keysym == 'Up':
            if selected_index:
                contacts_listbox.selection_clear(selected_index[0])
                contacts_listbox.selection_set(selected_index[0] - 1)
        elif event.keysym == 'Down':
            if selected_index:
                contacts_listbox.selection_clear(selected_index[0])
                contacts_listbox.selection_set(selected_index[0] + 1)
        elif event.keysym == 'Return':
            open_contact_info(event)

    # Bind the arrow keys to the listbox for scrolling
    contacts_listbox.bind("<Up>", on_arrow_key)
    contacts_listbox.bind("<Down>", on_arrow_key)

    # Enter the Tkinter event loop
    contacts_window.mainloop()


# Main function
def main():
    # Replace 'Carnet_a.sqlite' with the actual name of your SQLite database file
    database = "Carnet_a.sqlite"

    # Create a connection to the SQLite database
    global connection
    connection = create_connection(database)

    if connection:
        root = tk.Tk()
        root.title("Main Menu")
        root.geometry("300x300")

        # Create a Tkinter listbox for displaying menu options
        options_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        options_listbox.pack(expand=tk.YES, fill=tk.BOTH)

        # Add options to the listbox
        options = ["Add New Contact", "Display Contacts", "Exit"]
        for option in options:
            options_listbox.insert(tk.END, option)

        # Function to handle scrolling with arrow keys for the main menu
        def on_menu_arrow_key(event):
            if event.keysym == 'Up':
                selected_index = options_listbox.curselection()
                if selected_index:
                    options_listbox.selection_clear(selected_index[0])
                    options_listbox.selection_set(selected_index[0] - 1)
            elif event.keysym == 'Down':
                selected_index = options_listbox.curselection()
                if selected_index:
                    options_listbox.selection_clear(selected_index[0])
                    options_listbox.selection_set(selected_index[0] + 1)
            elif event.keysym == 'Return':
                selected_option = options_listbox.get(options_listbox.curselection())
                if selected_option == "Add New Contact":
                    add_contact_from_user_input(connection)
                elif selected_option == "Display Contacts":
                    display_contacts(connection)
                elif selected_option == "Exit":
                    root.destroy()

        # Bind the arrow keys to the listbox for scrolling on the main menu
        options_listbox.bind("<Up>", on_menu_arrow_key)
        options_listbox.bind("<Down>", on_menu_arrow_key)
        options_listbox.bind("<Return>", on_menu_arrow_key)

        root.mainloop()

        # Close the database connection
        connection.close()


# Run the main function if this script is the main module
if __name__ == "__main__":
    main()
