import sqlite3


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


# Function to edit the information of an existing contact
def edit_contact(connection, contact_id):
    try:
        cursor = connection.cursor()

        # Check if the contact with the given ID exists
        cursor.execute("SELECT * FROM Contact WHERE Contact_ID=?", (contact_id,))
        existing_contact = cursor.fetchone()

        if existing_contact:
            # Display existing contact details
            print("Existing Contact Details:")
            print("Contact ID:", existing_contact[0])
            print("Last Name:", existing_contact[1])
            print("First Name:", existing_contact[2])
            print("Date of Birth ID:", existing_contact[3])
            print("Email Address:", existing_contact[4])
            print("Phone Number:", existing_contact[5])
            print("Address ID:", existing_contact[6])
            print()

            # Get updated information from the user
            nom = input("Enter the updated last name (Press Enter to keep the existing value): ") or existing_contact[1]
            prenom = input("Enter the updated first name (Press Enter to keep the existing value): ") or \
                     existing_contact[2]
            jour = int(
                input("Enter the updated day of birth (Press Enter to keep the existing value): ") or existing_contact[
                    3])
            mois = int(input("Enter the updated month of birth (Press Enter to keep the existing value): ") or
                       existing_contact[4])
            annee = int(
                input("Enter the updated year of birth (Press Enter to keep the existing value): ") or existing_contact[
                    5])
            address_email = input("Enter the updated email address (Press Enter to keep the existing value): ") or \
                            existing_contact[6]
            numero_telephone = input("Enter the updated phone number (Press Enter to keep the existing value): ") or \
                               existing_contact[7]
            numero_et_rue = input("Enter the updated street address (Press Enter to keep the existing value): ") or \
                            existing_contact[8]
            ville = input("Enter the updated city (Press Enter to keep the existing value): ") or existing_contact[9]
            code_postal = input("Enter the updated postal code (Press Enter to keep the existing value): ") or \
                          existing_contact[10]

            # Update date of birth
            cursor.execute("UPDATE DateDeNaissance SET Jour=?, Mois=?, Annee=? WHERE DateDeNaissance_ID=?",
                           (jour, mois, annee, existing_contact[3]))

            # Update address
            cursor.execute("UPDATE Address SET NumeroEtRue=?, Ville=?, CodePostal=? WHERE Address_ID=?",
                           (numero_et_rue, ville, code_postal, existing_contact[8]))

            # Update contact information
            cursor.execute("""
                UPDATE Contact
                SET Nom=?, Prenom=?, DateDeNaissance_ID=?, AddressEmail=?, NumeroDeTelephone=?, Address_ID=?
                WHERE Contact_ID=?
            """, (nom, prenom, existing_contact[3], address_email, numero_telephone, existing_contact[8], contact_id))

            connection.commit()
            print("Contact updated successfully!")

        else:
            print("Contact with ID {} not found.".format(contact_id))

    except sqlite3.Error as e:
        connection.rollback()
        print("Error editing contact:", e)

    finally:
        cursor.close()


# Main function
def main():
    # Replace 'Carnet_a.sqlite' with the actual name of your SQLite database file
    database = "Carnet_a.sqlite"

    # Create a connection to the SQLite database
    connection = create_connection(database)

    if connection:
        print("Welcome to Gabriel's Address Book!")

        while True:
            print("\nMenu:")
            print("1. Add new contact")
            print("2. Edit existing contact")
            print("3. Exit")

            choice = input("Enter your choice (1, 2, or 3): ")

            if choice == "1":
                # Add new contact
                add_contact_from_user_input(connection)

            elif choice == "2":
                # Edit existing contact
                edit_contact_from_user_input(connection)

            elif choice == "3":
                # Exit the program
                break

            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

        # Close the database connection
        connection.close()


# Function to add a new contact using user input
def add_contact_from_user_input(connection):
    # Get user input for adding a new contact
    nom = input("Enter the last name: ")
    prenom = input("Enter the first name: ")
    jour = int(input("Enter the day of birth: "))
    mois = int(input("Enter the month of birth: "))
    annee = int(input("Enter the year of birth: "))
    address_email = input("Enter the email address: ")
    numero_telephone = input("Enter the phone number: ")
    numero_et_rue = input("Enter the street address: ")
    ville = input("Enter the city: ")
    code_postal = input("Enter the postal code: ")

    # Call the add_contact function to add the new contact to the database
    add_contact(
        connection,
        nom,
        prenom,
        jour,
        mois,
        annee,
        address_email,
        numero_telephone,
        numero_et_rue,
        ville,
        code_postal
    )


def edit_contact_from_user_input(connection):
    # Get user input for editing an existing contact
    contact_id_to_edit = int(input("Enter the Contact ID to edit: "))

    try:
        cursor = connection.cursor()

        # Check if the contact with the given ID exists
        cursor.execute("SELECT * FROM Contact WHERE Contact_ID=?", (contact_id_to_edit,))
        existing_contact = cursor.fetchone()

        if existing_contact:
            # Convert the tuple to a dictionary for flexible indexing
            existing_contact_dict = {
                "Contact_ID": existing_contact[0],
                "Last_Name": existing_contact[1],
                "First_Name": existing_contact[2],
                "Date_of_Birth_ID": existing_contact[3],
                "Email_Address": existing_contact[4],
                "Phone_Number": existing_contact[5],
                "Address_ID": existing_contact[6],
            }

            print("\nExisting Contact Details:")
            print("Contact ID:", existing_contact_dict["Contact_ID"])
            print("Last Name:", existing_contact_dict["Last_Name"])
            print("First Name:", existing_contact_dict["First_Name"])
            print("Date of Birth ID:", existing_contact_dict["Date_of_Birth_ID"])
            print("Email Address:", existing_contact_dict["Email_Address"])
            print("Phone Number:", existing_contact_dict["Phone_Number"])
            print("Address ID:", existing_contact_dict["Address_ID"])

            while True:
                print("\nMenu:")
                print("1. Edit Last Name")
                print("2. Edit First Name")
                print("3. Edit Date of Birth")
                print("4. Edit Email Address")
                print("5. Edit Phone Number")
                print("6. Edit Address")
                print("7. Done Editing")

                choice = input("Enter your choice (1-7): ")

                if choice == "1":
                    existing_contact_dict["Last_Name"] = input("Enter the updated last name: ")

                elif choice == "2":
                    existing_contact_dict["First_Name"] = input("Enter the updated first name: ")

                elif choice == "3":
                    existing_contact_dict["Date_of_Birth_ID"] = int(input("Enter the updated day of birth: "))

                elif choice == "4":
                    existing_contact_dict["Email_Address"] = input("Enter the updated email address: ")

                elif choice == "5":
                    existing_contact_dict["Phone_Number"] = input("Enter the updated phone number: ")

                elif choice == "6":
                    # Allow editing the address information
                    existing_contact_dict["Address_ID"] = edit_address_information(existing_contact_dict["Address_ID"])

                elif choice == "7":
                    # Update the contact information in the database
                    edit_contact(
                        connection,
                        contact_id_to_edit,
                        existing_contact_dict["Last_Name"],
                        existing_contact_dict["First_Name"],
                        existing_contact_dict["Date_of_Birth_ID"],
                        existing_contact_dict["Email_Address"],
                        existing_contact_dict["Phone_Number"],
                        existing_contact_dict["Address_ID"]
                    )
                    break

                else:
                    print("Invalid choice. Please enter a number between 1 and 7.")

        else:
            print("Contact with ID {} not found.".format(contact_id_to_edit))

    except sqlite3.Error as e:
        connection.rollback()
        print("Error editing contact:", e)

    finally:
        cursor.close()


# Function to edit address information using user input
def edit_address_information(existing_address_id):
    print("\nEdit Address:")
    print("1. Edit Street Address")
    print("2. Edit City")
    print("3. Edit Postal Code")
    print("4. Done Editing Address")

    address_choice = input("Enter your choice (1-4): ")

    if address_choice == "1":
        updated_street_address = input("Enter the updated street address: ")
        return update_address(existing_address_id, "NumeroEtRue", updated_street_address)

    elif address_choice == "2":
        updated_city = input("Enter the updated city: ")
        return update_address(existing_address_id, "Ville", updated_city)

    elif address_choice == "3":
        updated_postal_code = input("Enter the updated postal code: ")
        return update_address(existing_address_id, "CodePostal", updated_postal_code)

    elif address_choice == "4":
        return existing_address_id

    else:
        print("Invalid choice. Please enter a number between 1 and 4.")
        return edit_address_information(existing_address_id)


# Function to update specific fields in the Address table
def update_address(existing_address_id, field, new_value):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE Address SET {}=? WHERE Address_ID=?".format(field), (new_value, existing_address_id))
        connection.commit()
        print("Address information updated successfully.")
        return existing_address_id

    except sqlite3.Error as e:
        connection.rollback()
        print("Error updating address information:", e)
        return existing_address_id

    finally:
        cursor.close()


# Run the main function if this script is the main module
if __name__ == "__main__":
    main()
