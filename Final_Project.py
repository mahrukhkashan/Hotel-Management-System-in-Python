from logging import root
from tkinter import messagebox, Label, Spinbox, Button, Entry, Toplevel, Tk
from tkinter.ttk import Treeview

from PyQt5.QtWidgets import QComboBox, QApplication, QMessageBox, QMainWindow, QInputDialog, QLineEdit, QDialog, \
    QVBoxLayout, QPushButton, QTableWidgetItem, \
    QTableWidget, QSizePolicy, QLabel, QWidget, QSpinBox
from PyQt5 import uic
import csv
import hashlib
from collections import OrderedDict


class Guest:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
        self.full_name = ""
        self.age = 0
        self.city = ""
        self.contact_number = 0
        self.house = ""
        self.area = ""
        self.booked_floor = 0
        self.booked_room_type = ""
        self.booked_room_number = 0
        self.total_days = 0
        # self.rooms_bill =0
        # self.days = 0
        self.total_bill = 0

    def set_booking_info(self, floor, room_type, room_number):
        self.booked_floor = floor
        self.booked_room_type = room_type
        self.booked_room_number = room_number


class ModifyAttributeDialog(QDialog):
    def __init__(self, attribute_name, parent=None):
        super(ModifyAttributeDialog, self).__init__(parent)
        self.setWindowTitle(f"Modify {attribute_name.capitalize()}")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.label = QLineEdit(self)
        self.label.setPlaceholderText(f"Enter new {attribute_name.lower()}")

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)

        layout.addWidget(self.label)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

class TreeNode:
    def __init__(self, username, data=None):
        self.username = username
        self.data = data
        self.left_child = None
        self.right_child = None

class HotelManagementSystem:
    def __init__(self):
        self.admin_username = 'admin'
        self.admin_password = 'adminpass'
        self.guest_file = 'guest_data.csv'
        self.guest_data = {}
        self.load_guest_data()
        self.root = Tk()

        self.root_ac = None
        self.root_non_ac = None

        self.room_booking_system = RoomBookingSystem()

        self.menu_file = 'room_service_menu.csv'
        self.order_items = {}
        self.menu_data = {}
        self.load_menu_from_csv()

        self.welcome_ui = self.load_ui('welcome.ui')
        self.signin_ui = self.load_ui('Sign-in.ui')
        self.signup_ui = self.load_ui('sign_up.ui')
        self.personal_info_ui = self.load_ui('personal_information.ui')
        self.guest_menu_ui = self.load_ui('guest_menu.ui')
        self.ac_ui = self.load_ui('ac_nonac.ui')
        self.groundfloors_ui = self.load_ui('groundfloor.ui')
        self.topfloors_ui = self.load_ui('topfloor.ui')
        self.rooms_ui = self.load_ui('rooms.ui')
        self.admin_menu_ui = self.load_ui('admin_menu.ui')
        self.check_in_ui = self.load_ui('Check_IN.ui')
        self.viewRooms_ui = self.load_ui('view_rooms.ui')
        self.room_service_ui = self.load_ui('food_menu.ui')
        self.View_Guest_ui = self.load_ui('view_guest_info.ui')
        self.check_out_ui = self.load_ui('checkOut.ui')
        self.guest_data_bst = OrderedDict()
        self.setup_connections()

        self.welcome_ui.show()
        self.welcome_ui.next_button.clicked.connect(self.show_signin_page)
       # self.guest_data_bst = None
    def setup_connections(self):
        # Connect signals to slots
        self.signin_ui.sign_in_button.clicked.connect(self.perform_signin_clicked)
        self.signin_ui.sign_up_button.clicked.connect(self.show_signup_page)
        self.signup_ui.sign_up_button2.clicked.connect(self.show_personal_info_page)
        self.personal_info_ui.DoneButton.clicked.connect(self.save_personal_info)

        self.ac_ui.acButton.clicked.connect(self.show_topfloor_form)
        self.ac_ui.nonacButton.clicked.connect(self.show_groundfloor_form)

        self.groundfloors_ui.floor1Button.clicked.connect(self.show_ground_floor_rooms)
        self.groundfloors_ui.floor2Button.clicked.connect(self.show_ground_floor_rooms)
        self.groundfloors_ui.floor3Button.clicked.connect(self.show_ground_floor_rooms)
        self.groundfloors_ui.floor4Button.clicked.connect(self.show_ground_floor_rooms)
        self.groundfloors_ui.floor5Button.clicked.connect(self.show_ground_floor_rooms)

        self.topfloors_ui.floor6Button.clicked.connect(self.show_top_floor_rooms)
        self.topfloors_ui.floor7Button.clicked.connect(self.show_top_floor_rooms)
        self.topfloors_ui.floor8Button.clicked.connect(self.show_top_floor_rooms)
        self.topfloors_ui.floor9Button.clicked.connect(self.show_top_floor_rooms)
        self.topfloors_ui.floor10Button.clicked.connect(self.show_top_floor_rooms)

        self.admin_menu_ui.guestButton.clicked.connect(self.show_guest_info)
        self.admin_menu_ui.exitButton.clicked.connect(self.show_signin_page)
        self.guest_menu_ui.ExitButton.clicked.connect(self.show_signin_page)

        self.ac_ui.acButton.clicked.connect(self.show_topfloor_form)
        self.ac_ui.nonacButton.clicked.connect(self.show_groundfloor_form)

        self.guest_menu_ui.ViewRoomsButton.clicked.connect(self.show_view_rooms_form)
        self.guest_menu_ui.checkOutButton.clicked.connect(self.display_checkout_table)

        self.guest_menu_ui.RoomServiceButton.clicked.connect(self.show_room_service_menu)
        self.room_service_ui.placeOrderButton.clicked.connect(self.place_order)
        self.room_service_ui.backButton.clicked.connect(self.show_guest_menu)
        self.View_Guest_ui.backButtonView.clicked.connect(self.ShowAdminPage)
        self.View_Guest_ui.removeButton.clicked.connect(self.remove_guest_button_clicked)
        self.View_Guest_ui.modifyButton.clicked.connect(self.show_modify_dialog)
        self.View_Guest_ui.searchButton.clicked.connect(self.search_button_clicked)
        self.View_Guest_ui.sort_button.clicked.connect(self.sort_guest_data)


    def load_ui(self, file_path):
        ui = uic.loadUi(file_path)
        return ui

    def load_guest_data(self):
        try:
            with open(self.guest_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    username = row['username']
                    if username not in self.guest_data:
                        self.guest_data[username] = Guest(
                            username, row['password_hash']
                        )
                        guest = self.guest_data[username]
                        guest.full_name = row.get('full_name', '')
                        guest.age = int(row.get('age', 0))
                        guest.city = row.get('city', '')
                        guest.contact_number = row.get('contact_number', '')
                        guest.house = row.get('house', '')
                        guest.area = row.get('area', '')
                        guest.booked_floor = int(row.get('booked_floor', 0))
                        guest.booked_room_type = row.get('booked_room_type', '')
                        guest.booked_room_number = int(row.get('booked_room_number', 0))
                        guest.total_days = int(row.get('total_days', 0))
                        # guest.rooms_bill = int(row.get('rooms_bill', 0))
                        guest.total_bill = int(row.get('total_bill', 0))

        except FileNotFoundError:
            pass


    def save_guest_data_to_csv(self):
        try:
            with open(self.guest_file, 'w', newline='') as file:
                fieldnames = ['username', 'password_hash', 'full_name', 'age', 'city', 'contact_number', 'house',
                              'area', 'booked_floor', 'booked_room_type', 'booked_room_number', 'total_days', 'total_bill', 'payment_method', 'rating']
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                # Check if the file is empty, and write the header if needed
                if file.tell() == 0:
                    writer.writeheader()

                for guest in self.guest_data.values():
                    writer.writerow({
                        'username': guest.username,
                        'password_hash': guest.password_hash,
                        'full_name': guest.full_name,
                        'age': guest.age,
                        'city': guest.city,
                        'contact_number': guest.contact_number,
                        'house': guest.house,
                        'area': guest.area,
                        'booked_floor': guest.booked_floor,
                        'booked_room_type': guest.booked_room_type,
                        'booked_room_number': guest.booked_room_number,
                        'total_days': guest.total_days,
                        'total_bill': guest.total_bill,
                        'payment_method': guest.payment_method,
                        'rating': guest.rating
                    })

        except Exception as e:
            print(f"Exception in save_guest_data_to_csv: {e}")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()


    def display_guest_info(self, data):
        try:
            if not data:
                QMessageBox.information(self.View_Guest_ui, "No Matching Rows", "No matching rows found.")
                return

            # Assuming all objects in the list have the same attributes
            attributes = list(vars(data[0]).keys())

            self.View_Guest_ui.tableWidget.setColumnCount(len(attributes))
            self.View_Guest_ui.tableWidget.setRowCount(len(data))

            for row, guest in enumerate(data):
                for col, attr in enumerate(attributes):
                    value = getattr(guest, attr, 'N/A')
                    item = QTableWidgetItem(str(value))
                    self.View_Guest_ui.tableWidget.setItem(row, col, item)

        except Exception as e:
            QMessageBox.critical(self.View_Guest_ui, "Error", f"An error occurred: {str(e)}")

    def search_data(self, search_term, mode="username"):
        try:
            if not self.guest_data:
                QMessageBox.warning(self.View_Guest_ui, "Data not loaded", "Guest data is not loaded.")
                return

            search_term = search_term.lower()

            if not search_term:
                QMessageBox.warning(self.View_Guest_ui, "Empty Search Term", "Please enter a search term.")
                return

            data = self.guest_data.values()

            # Use "mode" argument to define search criteria
            if mode == "username":
                matching_rows = [guest for guest in data if isinstance(guest, Guest) and
                                 search_term in guest.username.lower()]
            elif mode == "other":
                selected_column = self.View_Guest_ui.ColumnComboBox.currentText().lower()
                if not selected_column:
                    QMessageBox.warning(self.View_Guest_ui, "No Column Selected", "Please select a column to search.")
                    return

                # Use this block to search based on selected column
                matching_rows = [guest for guest in data if isinstance(guest, Guest) and
                                 search_term in str(getattr(guest, selected_column, '')).lower()]
            else:
                raise ValueError(f"Invalid search mode: {mode}")

            self.display_search_results(matching_rows)

        except Exception as e:
            QMessageBox.critical(self.View_Guest_ui, "Search Error", f"An error occurred during the search: {str(e)}")

    def search_button_clicked(self):
        try:
            username_to_search = self.View_Guest_ui.usernameLineEdit.text().strip()
            self.search_data(username_to_search, mode="username")
        except Exception as e:
            print(f"Exception in search_button_clicked: {e}")
            QMessageBox.critical(None, 'Error', f'An error occurred: {str(e)}')

    def display_search_results(self, matching_rows):
        try:
            rows = len(matching_rows)
            if rows == 0:
                QMessageBox.information(self.View_Guest_ui, "No Matching Rows", "No matching rows found.")
                return

            cols = len(vars(matching_rows[0]))
            self.View_Guest_ui.tableWidget.setRowCount(rows)
            self.View_Guest_ui.tableWidget.setColumnCount(cols)

            for row, guest in enumerate(matching_rows):
                for col, (attr, value) in enumerate(vars(guest).items()):
                    item = QTableWidgetItem(str(value))
                    self.View_Guest_ui.tableWidget.setItem(row, col, item)
        except AttributeError as e:
            QMessageBox.critical(self.View_Guest_ui, "Attribute Error",
                                 f"AttributeError: {str(e)} - Check attribute names.")
        except IndexError as e:
            QMessageBox.critical(self.View_Guest_ui, "Index Error", f"IndexError: {str(e)} - Check list indices.")

    def sort_guest_data(self):
        try:
            # Convert the dictionary values to a list for sorting
            guest_list = list(self.guest_data.values())

            # Sort the data using the sorted function
            guest_list = sorted(guest_list, key=lambda guest: guest.username)

            # Clear existing data in the table
            self.View_Guest_ui.tableWidget.clearContents()

            # Display the sorted data
            self.display_search_results(guest_list)

            QMessageBox.information(self.View_Guest_ui, "Sort Successful", "Data sorted by username.")
        except Exception as e:
            QMessageBox.critical(self.View_Guest_ui, "Sort Error", f"An error occurred during sorting: {str(e)}")

    def ShowAdminPage(self):
        self.View_Guest_ui.hide()
        self.admin_menu_ui.show()

    def remove_guest(self, username):
        try:
            if username in self.guest_data:
                del self.guest_data[username]
                self.save_guest_data_to_csv()
                return True, f"Guest '{username}' has been successfully removed."
            else:
                return False, f"Guest '{username}' not found."
        except Exception as e:
            return False, f"An error occurred: {str(e)}"

    def remove_guest_button_clicked(self):
        try:
            # Retrieve the username from the QLineEdit
            username_to_remove = self.View_Guest_ui.usernameLineEdit.text().strip()

            # Check if the username exists in the guest data
            if username_to_remove in self.guest_data:
                # Remove the user from the guest data
                success, message = self.remove_guest(username_to_remove)

                # Show a dialog box based on the removal result
                if success:
                    QMessageBox.information(None, 'Removal Successful', message)
                    # Refresh the guest info table
                    self.show_guest_info()
                else:
                    QMessageBox.warning(None, 'Removal Failed', message)
            else:
                QMessageBox.warning(None, 'User Not Found', f"The user '{username_to_remove}' does not exist.")

        except Exception as e:
            print(f"Exception in remove_guest_button_clicked: {e}")
            QMessageBox.critical(None, 'Error', f'An error occurred: {str(e)}')

    def show_modify_dialog(self):
        # Get the username from the QLineEdit
        username_to_modify = self.View_Guest_ui.usernameLineEdit.text().strip()

        # Check if the username exists in the guest data
        if username_to_modify in self.guest_data:
            # Get the attribute names for the combo box
            attribute_names = ['Full Name', 'Age', 'City', 'Contact Number', 'House', 'Area']

            # Ask the user to choose an attribute
            attribute, ok = QInputDialog.getItem(None, 'Select Attribute', 'Choose an attribute to modify:',
                                                 attribute_names, 0, False)
            if not ok:
                # User canceled the modification
                return

            # Open a dialog to get the new value for the chosen attribute
            dialog = ModifyAttributeDialog(attribute)
            if dialog.exec_() == QDialog.Accepted:
                new_value = dialog.label.text()
            else:
                # User canceled the modification
                return

            # Update the selected attribute with the new value
            setattr(self.guest_data[username_to_modify], attribute.lower().replace(" ", "_"), new_value)
            self.save_guest_data_to_csv()
            # Show a message box indicating successful modification
            QMessageBox.information(None, 'Modification Successful',
                                    f"User '{username_to_modify}' has been successfully modified.")
        else:
            QMessageBox.warning(None, 'User Not Found', f"The user '{username_to_modify}' does not exist.")
        self.show_guest_info()

    def open_admin_menu(self):
        # Add code to open the admin menu UI form here
        self.signin_ui.hide()
        self.admin_menu_ui.show()

    def show_signin_page(self):
        self.welcome_ui.hide()
        self.signin_ui.show()
        self.signin_ui.usernameInput.setFocus()  # Set focus on the username line edit

    def show_signup_page(self):
        self.signin_ui.hide()
        self.signup_ui.show()
        self.signup_ui.usernameInput.setFocus()  # Set focus on the username input field

        # Connect the correct method to the Sign Up button
        self.signup_ui.sign_up_button2.clicked.connect(self.perform_signup_clicked)

    def perform_signin_clicked(self):
        try:
            username = self.signin_ui.usernameInput.text()
            password = self.signin_ui.passwordInput.text()

            # Check if both username and password are entered
            if not username or not password:
                QMessageBox.warning(None, 'Sign-In Error', 'Please enter both username and password.')
                return

            # Check if the entered credentials match the admin credentials
            if username == self.admin_username and password == self.admin_password:
                QMessageBox.information(None, 'Admin Sign-In', 'Admin Sign-In Successful!')
                # Open the admin menu UI form here
                self.open_admin_menu()
                return

            # Check if the username exists in guest data
            if username not in self.guest_data:
                QMessageBox.warning(None, 'Sign-In Error',
                                    'Invalid username. Please sign up first or enter a valid username.')
                return

            # Check if the entered password matches the hashed password
            if self.validate_credentials(username, password):
                # Open the guest menu UI form here
                self.open_guest_menu()

            else:
                QMessageBox.warning(None, 'Sign-In Error',
                                    'Invalid password. Enter correct credentials or sign up first.')

        except Exception as e:
            print(f"Exception in sign_in_clicked: {e}")

    # Add this method to validate guest credentials
    def validate_credentials(self, username, password):
        # Check if the entered password matches the hashed password
        return self.guest_data[username].password_hash == self.hash_password(password)

    def perform_signup_clicked(self):
        try:
            username = self.signup_ui.usernameInput.text()
            password = self.signup_ui.passwordInput.text()

            # Check if both username and password are entered
            if not username or not password:
                QMessageBox.warning(None, 'Sign-Up Error', 'Please enter both username and password.')
                return

            # Validate username against existing users
            if username in self.guest_data:
                QMessageBox.warning(None, 'Sign-Up Error',
                                    'Username already exists. Please choose a different username.')
                # Don't proceed with the sign-up if the username already exists
                return

            # Validate password length
            if len(password) < 8:
                QMessageBox.warning(None, 'Sign-Up Error', 'Password must be at least 8 characters long.')
                return

            # Validate other password requirements if needed

            # Perform the signup
            guest = Guest(username, self.hash_password(password))
            guest.booking_system = RoomBookingSystem()  # Initialize the booking_system attribute
            self.guest_data[username] = guest  # Add the new guest to guest_data
            self.save_guest_data_to_csv()

            # Hide the signup UI
            self.signup_ui.hide()
            QMessageBox.information(None, 'Sign-Up Successful', 'User signed up successfully!')

            # Show the personal info page
            self.show_personal_info_page(username)

        except Exception as e:
            print(f"Exception in perform_signup_clicked: {e}")
            QMessageBox.critical(None, 'Error', f'An error occurred during sign-up: {str(e)}')
            # Show the signup UI again if there's an error
            self.signup_ui.show()

    def show_personal_info_page(self, username):
        try:
            # Hide the signup UI and show the personal info page
            self.signup_ui.show()
            if username in self.guest_data:
                QMessageBox.information(None, 'Sign-Up Successful', 'User signed up successfully!')

                # Show the personal info page only if there are no error messages
                self.signup_ui.hide()
                self.personal_info_ui.show()

        except Exception as e:
            print(f"Exception in show_personal_info_page: {e}")
            QMessageBox.critical(None, 'Error', f'An error occurred: {str(e)}')

    def save_personal_info(self):
        try:
            full_name = self.personal_info_ui.nameInput.text()
            age_text = self.personal_info_ui.ageInput.text()
            city = self.personal_info_ui.cityInput.text()
            contact_number = self.personal_info_ui.contactInput.text()
            house = self.personal_info_ui.houseInput.text()
            area = self.personal_info_ui.areaInput.text()

            # Validate that all fields are filled
            if not (full_name and age_text and city and contact_number and house and area):
                QMessageBox.warning(None, 'Personal Info Error', 'Please fill in all fields in the form.')
                return

            # Convert age to integer
            age = int(age_text) if age_text.isdigit() else 0

            # Validate contact number
            if not contact_number.isdigit() or len(contact_number) != 11:
                QMessageBox.warning(None, 'Personal Info Error',
                                    'Invalid contact number. Please enter a valid 11-digit number.')
                return

            # Save personal information to CSV or perform any other desired actions
            guest = self.guest_data.get(self.signup_ui.usernameInput.text())
            if guest:
                guest.full_name = full_name
                guest.age = age
                guest.city = city
                guest.contact_number = contact_number  # Save contact number as string
                guest.house = house
                guest.area = area
                self.save_guest_data_to_csv()

                self.personal_info_ui.hide()
                QMessageBox.information(None, 'Sign-Up Successful', 'User signed up successfully!')

                # Open the guest menu UI form here
                self.signin_ui.show()
                self.perform_signin_clicked()

            else:
                QMessageBox.critical(None, 'Error', 'Guest data not found.')

        except Exception as e:
            print(f"Exception in save_personal_info: {e}")
            QMessageBox.critical(None, 'Error', f'An error occurred while saving personal information: {str(e)}')

    def open_guest_menu(self):
        # Hide the current UI and show the guest menu UI
        self.signin_ui.hide()
        self.signup_ui.hide()
        self.personal_info_ui.hide()
        self.viewRooms_ui.hide()
        # self.guest_menu_ui.show()
        self.guest_menu_ui.show()

        # Connect the booking button to the method in GuestMenu
        self.guest_menu_ui.BookingButton.clicked.connect(self.guest_booking_clicked)
        self.guest_menu_ui.CheckInButton.clicked.connect(self.show_check_in_form)


    def guest_booking_clicked(self):
        # Check if the guest has already booked a room
        username = self.signin_ui.usernameInput.text()  # You may need to adjust this based on how you get the username
        guest = self.guest_data.get(username)

        if guest and guest.booked_floor and guest.booked_room_type and guest.booked_room_number:
            # Display information about the booked room
            QMessageBox.information(None, 'Booked Room Information',
                                    f'You have already booked a room!\nFloor: {guest.booked_floor}\n'
                                    f'Room Type: {guest.booked_room_type}\nRoom Number: {guest.booked_room_number}')
        else:
            # If not booked, proceed with the booking logic
            self.guest_menu_ui.hide()
            self.ac_ui.show()

    def book_room(self, floor, room_type):
        # Get the guest from the current session
        username = self.signin_ui.usernameInput.text()
        guest = self.guest_data.get(username)

        if guest:
            # Get available rooms for the selected room type and floor
            available_rooms = self.get_available_rooms(floor, room_type)

            if available_rooms:
                assigned_room = available_rooms[0]

                # Update the visited array for the assigned room
                self.update_visited_array(floor, room_type, assigned_room)

                # Update the guest's booking information
                guest.set_booking_info(floor, room_type, assigned_room)
                self.save_guest_data_to_csv()

                # Display a confirmation message
                ac_status = "Yes" if "ac" in room_type.lower() else "No"
                confirmation_message = f'Room booked successfully!\nType: {room_type}\nFloor: {floor}\n' \
                                       f'Room Number: {assigned_room}'
                QMessageBox.information(None, 'Room Booking', confirmation_message, QMessageBox.Ok)

                # Return to the guest menu UI
                self.open_guest_menu()

            else:
                QMessageBox.warning(None, 'Room Booking', 'No available rooms for the selected type and floor.')


    def show_ground_floor_rooms(self):
        self.groundfloors_ui.hide()
        self.rooms_ui.show()


    def show_top_floor_rooms(self):
        self.topfloors_ui.hide()
        self.rooms_ui.show()


    def show_topfloor_form(self):
        # Hide the AC form and show the top floor form
        self.ac_ui.hide()
        self.topfloors_ui.show()

        # Connect the buttons in the top floor form to room type selection methods
        self.topfloors_ui.floor6Button.clicked.connect(lambda: self.show_room_type_form(6))
        self.topfloors_ui.floor7Button.clicked.connect(lambda: self.show_room_type_form(7))
        self.topfloors_ui.floor8Button.clicked.connect(lambda: self.show_room_type_form(8))
        self.topfloors_ui.floor9Button.clicked.connect(lambda: self.show_room_type_form(9))
        self.topfloors_ui.floor10Button.clicked.connect(lambda: self.show_room_type_form(10))

    def show_groundfloor_form(self):
        # Hide the AC form and show the ground floor form
        self.ac_ui.hide()
        self.groundfloors_ui.show()

        # Connect the buttons in the ground floor form to room type selection methods
        self.groundfloors_ui.floor1Button.clicked.connect(lambda: self.show_room_type_form(1))
        self.groundfloors_ui.floor2Button.clicked.connect(lambda: self.show_room_type_form(2))
        self.groundfloors_ui.floor3Button.clicked.connect(lambda: self.show_room_type_form(3))
        self.groundfloors_ui.floor4Button.clicked.connect(lambda: self.show_room_type_form(4))
        self.groundfloors_ui.floor5Button.clicked.connect(lambda: self.show_room_type_form(5))

    def show_room_type_form(self, floor):

        # Connect the buttons in the room type form to room selection methods
        self.rooms_ui.doubleButton.clicked.connect(lambda: self.book_room(floor, 'Double Bed Room'))
        self.rooms_ui.standardButton.clicked.connect(lambda: self.book_room(floor, 'Standard Bed Room'))
        self.rooms_ui.executiveButton.clicked.connect(lambda: self.book_room(floor, 'Executive Bed Room'))
        self.rooms_ui.suiteButton.clicked.connect(lambda: self.book_room(floor, 'Suite Bed Room'))
        self.rooms_ui.familyButton.clicked.connect(lambda: self.book_room(floor, 'Family Bed Room'))

    def get_available_rooms(self, floor, room_type):
        # Get available rooms based on the visited array
        visited_array = self.get_visited_array(floor, room_type)
        available_rooms = [i + 1 for i, visited in enumerate(visited_array) if not visited]
        return available_rooms

    def get_visited_array(self, floor, room_type):
        # Get the visited array based on the guest's booking system
        guest = self.guest_data.get(self.signup_ui.usernameInput.text())
        if guest:
            booking_system = guest.booking_system
            return booking_system.get_visited_array(floor, room_type)
        return [False] * 5

    def update_visited_array(self, floor, room_type, room_number):
        # Update the visited array based on the guest's booking system
        guest = self.guest_data.get(self.signup_ui.usernameInput.text())
        if guest:
            booking_system = guest.booking_system
            booking_system.update_visited_array(floor, room_type, room_number)


    def show_booked_room_info(self):
        username = self.signin_ui.usernameInput.text()  # Assuming you are using this for the username
        guest = self.guest_data.get(username)

        if guest and guest.booked_floor and guest.booked_room_type and guest.booked_room_number:
            QMessageBox.information(None, 'Booked Room Information',
                                    f'You have already booked a room!\nFloor: {guest.booked_floor}\n'
                                    f'Room Type: {guest.booked_room_type}\nRoom Number: {guest.booked_room_number}')
        else:
            QMessageBox.information(None, 'Booked Room Information', 'You have not booked a room yet.')

    def show_guest_info(self):
        self.admin_menu_ui.hide()
        self.View_Guest_ui.show()
        try:
            # Load the CSV data
            with open(self.guest_file, 'r') as file:
                reader = csv.DictReader(file)

                # Set the number of rows and columns in the table
                self.View_Guest_ui.tableWidget.setRowCount(0)
                self.View_Guest_ui.tableWidget.setColumnCount(len(reader.fieldnames))

                # Set the horizontal header labels
                self.View_Guest_ui.tableWidget.setHorizontalHeaderLabels(reader.fieldnames)

                # Add data to the table
                for row_data in reader:
                    row_position = self.View_Guest_ui.tableWidget.rowCount()
                    self.View_Guest_ui.tableWidget.insertRow(row_position)
                    for column, value in enumerate(reader.fieldnames):
                        item = QTableWidgetItem(row_data[value])
                        self.View_Guest_ui.tableWidget.setItem(row_position, column, item)

        except FileNotFoundError:
            QMessageBox.warning(None, 'Warning', 'Guest data file not found.')

    def show_check_in_form(self):
        # Hide the current UI and show the check-in form
        self.guest_menu_ui.hide()

        # Show the check-in form
        self.check_in_ui.show()

        # Connect the confirm button to the method for check-in confirmation
        self.check_in_ui.ConfirmButton.clicked.connect(self.confirm_check_in)

    def confirm_check_in(self):
        try:
            # Get the entered username and validate it
            username = self.check_in_ui.usernameInput.text()
            guest = self.guest_data.get(username)
            self.check_in_ui.usernameInput.setFocus()

            if not guest:
                QMessageBox.warning(None, 'Check-In Error', 'Invalid username. Please enter a valid username.')
                return

            # Retrieve the booked room type from the CSV
            booked_room_type = guest.booked_room_type

            if not booked_room_type:
                QMessageBox.warning(None, 'Check-In Error', 'Please book a room before checking in.')
                return

            # Get the number of days and validate it
            days_text = self.check_in_ui.daysInput.text()
            if not days_text.isdigit():
                QMessageBox.warning(None, 'Check-In Error', 'Please enter a valid number of days.')
                return

            if guest.booked_floor and guest.booked_room_number:
                # Calculate the total bill based on booked room type and number of days
                total_days = int(days_text)
                total_bill = self.calculate_total_bill(booked_room_type, total_days)

                # Save the total bill to the guest details CSV file
                self.save_total_bill_to_csv(username, total_bill, total_days)

                # Display the total bill to the user
                QMessageBox.information(self.check_in_ui, 'Check-In Confirmation',
                                        f'Check-In successful!\nTotal Bill: {total_bill} USD')

                # Return to the guest menu UI
                self.open_guest_menu()

                # Close the check-in form
                self.check_in_ui.accept()

            else:
                QMessageBox.warning(None, 'Check-In Error', 'You have not booked a room yet.')

        except Exception as e:
            print(f"Exception in confirm_check_in: {e}")
            QMessageBox.critical(None, 'Error', f'An error occurred during check-in: {str(e)}')

    def calculate_total_bill(self, room_type, total_days):
        # You need to implement your own logic for calculating the total bill here
        # Multiply the daily rate based on the room type with the total number of days
        if room_type == 'Standard Bed Room':
            daily_rate = 200
        elif room_type == 'Double Bed Room':
            daily_rate = 500
        elif room_type == 'Family Bed Room':
            daily_rate = 1000
        elif room_type == 'Executive Bed Room':
            daily_rate = 1500
        elif room_type == 'Suite Bed Room':
            daily_rate = 2000
        else:
            # Handle the case where the room type is unknown
            raise ValueError(f'Unknown room type: {room_type}')

        # Calculate the total bill
        total_bill = daily_rate * total_days

        return total_bill

    # Add a new method to save the total bill to the CSV file
    def save_total_bill_to_csv(self, username, total_bill, total_days):
        try:
            # Load existing data from CSV file
            with open('guest_data.csv', 'r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            # Find the row corresponding to the username
            for row in rows:
                if row['username'] == username:
                    # Update the total_days and total_bill in the row
                    row['total_days'] = str(total_days)
                    row['total_bill'] = str(total_bill)

                    break

            # Save the updated data back to the CSV file
            with open('guest_data.csv', 'w', newline='') as file:
                fieldnames = reader.fieldnames + ['total_days', 'total_bill']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

        except Exception as e:
            print(f"Exception in save_total_bill_to_csv: {e}")
            QMessageBox.critical(None, 'Error', f'An error occurred while saving the total bill: {str(e)}')

    def show_view_rooms_form(self):
        # Hide the current UI and show the view_rooms.ui form
        self.guest_menu_ui.hide()

        # Create an instance of the view_rooms.ui form
        self.viewRooms_ui = self.load_ui('view_rooms.ui')

        # Show the view_rooms.ui form
        self.viewRooms_ui.show()

        # Connect the backButton to the method for going back to the guest_menu_ui
        self.viewRooms_ui.backButton.clicked.connect(self.open_guest_menu)

    def load_menu_from_csv(self):
        try:
            with open(self.menu_file, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)  # Skip header
                for row in reader:
                    self.menu_data[row[0]] = int(row[1])

        except FileNotFoundError:
            print(f"Menu file '{self.menu_file}' not found.")
        except Exception as e:
            print(f"Exception in load_menu_from_csv: {e}")

    def save_menu_to_csv(self):
        try:
            with open(self.menu_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Item', 'Price'])

                for item, price in self.menu_data.items():
                    writer.writerow([item, price])

            print(f"Menu data saved to '{self.menu_file}' successfully!")
        except Exception as e:
            print(f"Exception in save_menu_to_csv: {e}")

    def show_room_service_menu(self):

        self.guest_menu_ui.hide()
        self.room_service_ui.show()

    def show_guest_menu(self):

        self.room_service_ui.hide()
        self.guest_menu_ui.show()

    def save_room_service_payment(self, total_cost):

        username = self.signin_ui.usernameInput.text()  # You may need to adjust this based on how you get the username
        guest = self.guest_data.get(username)

        try:

            if guest in self.guest_data:
                guest = self.guest_data[self.username]
                guest.payment = total_cost
                self.save_guest_data_to_csv()

        except Exception as e:
            print(f"Exception in save_room_service_payment: {e}")
            QMessageBox.critical(None, 'Error', f'An error occurred while saving payment: {str(e)}')

    def place_order(self, username):

        username = self.signin_ui.usernameInput.text()  # You may need to adjust this based on how you get the username
        guest = self.guest_data.get(username)

        try:
            menu_table = self.room_service_ui.menuTableWidget

            available_items = {}
            for row in range(menu_table.rowCount()):
                item_name = menu_table.item(row, 0).text()
                item_price = int(menu_table.item(row, 1).text())
                available_items[item_name] = item_price

            order_confirmation = QMessageBox.question(
                None, "Order Confirmation", "Would you like to place an order?", QMessageBox.Yes | QMessageBox.No)

            if order_confirmation == QMessageBox.Yes:
                while True:
                    item, ok = QInputDialog.getItem(
                        None, "Select Item", "Choose an item to order:", list(available_items.keys()), 0, False)

                    if ok:
                        # Check if the item is already in the order, if so, increment the quantity
                        if item in self.order_items:
                            self.order_items[item] += 1
                        else:
                            self.order_items[item] = 1  # Initialize quantity for new items

                        add_more = QMessageBox.question(
                            None, "Add More Items", "Do you want to order more items?",
                            QMessageBox.Yes | QMessageBox.No)
                        if add_more == QMessageBox.No:
                            break
                    else:
                        break

                total_cost = sum(self.order_items[item] * available_items[item] for item in self.order_items)
                self.save_room_service_payment(total_cost)

                payment_message = f"Ordered items: {', '.join(f'{item} x{self.order_items[item]}' for item in self.order_items)}\nTotal Cost: ${total_cost}"
                QMessageBox.information(None, 'Order Placed', payment_message)

        except Exception as e:
            print(f"Exception in place_order: {e}")
            QMessageBox.critical(None, 'Error', f'An error occurred while placing order: {str(e)}')
        # Add this method to your HotelManagementSystem class

    def show_check_out_form(self):
        if self.guest_menu_ui:
            self.guest_menu_ui.hide()  # Replace hide() with the appropriate method
            self.display_checkout_table()

    def display_checkout_table(self):
        try:
            # Create a new window for displaying the checkout table
            checkout_window = QWidget()
            checkout_window.setWindowTitle("Checkout Details")

            # Create a layout for checkout details
            layout = QVBoxLayout(checkout_window)
            layout.addWidget(QLabel("Checkout Details:"))

            # Populate the checkout details
            for guest in self.guest_data.values():
                checkout_label = QLabel(
                    f"Username: {guest.username}, Full Name: {guest.full_name}, "
                    f"Room Type: {guest.booked_room_type}, Room Number: {guest.booked_room_number}, "
                    f"Total Bill: {guest.total_bill}"
                )
                layout.addWidget(checkout_label)

            # Create a button to proceed to payment
            payment_button = QPushButton("Make Payment")
            payment_button.clicked.connect(lambda: self.process_payment(checkout_window))
            layout.addWidget(payment_button)

            checkout_window.show()

        except Exception as e:
            print(f"Exception in show_guest_details: {e}")

    def process_payment(self, checkout_window):
        # Create a new window for payment and rating details
        payment_window = QWidget()
        payment_window.setWindowTitle("Payment and Rating Details")

        # Create a layout for payment details
        layout = QVBoxLayout(payment_window)
        layout.addWidget(QLabel("Payment Method:"))
        payment_method_entry = QLineEdit()
        layout.addWidget(payment_method_entry)

        # Create a layout for rating details
        layout.addWidget(QLabel("Rating (1-5):"))
        rating_spinbox = QSpinBox()
        rating_spinbox.setRange(1, 5)
        layout.addWidget(rating_spinbox)

        # Create a button to confirm payment and rating
        confirm_button = QPushButton("Confirm Payment and Rating")
        confirm_button.clicked.connect(lambda: self.confirm_payment_and_rating(payment_window, payment_method_entry,
                                                                               rating_spinbox, checkout_window))
        layout.addWidget(confirm_button)

        payment_window.show()

    def confirm_payment_and_rating(self, payment_window, payment_method_entry, rating_spinbox, checkout_window):
        # Get payment method and rating from entry widgets
        payment_method = payment_method_entry.text()
        rating = str(rating_spinbox.value())

        # For simplicity, assume payment is always successful
        QMessageBox.information(payment_window, "Payment and Rating", f"Payment successful!\nRating: {rating}")

        # Close the payment window and checkout window
        payment_window.close()
        checkout_window.close()

        # Show a success message (you can customize this message)
        QMessageBox.information(self, "Checkout Successful", "Checkout completed successfully!")

class RoomTypeNode:
    def __init__(self, room_type, floor):
        self.room_type = room_type
        self.floor = floor
        self.visited_array = {}  # Dictionary to store visited status for each room number
        self.left = None
        self.right = None
class RoomBookingSystem:
    def __init__(self):
        self.root_ac = None
        self.root_non_ac = None

    def insert_room_type(self, room_type, floor, ac=True):
        if ac:
            self.root_ac = self._insert_room_type(self.root_ac, room_type, floor)
        else:
            self.root_non_ac = self._insert_room_type(self.root_non_ac, room_type, floor)

    def _insert_room_type(self, node, room_type, floor):
        if not node:
            return RoomTypeNode(room_type, floor)

        if floor < node.floor:
            node.left = self._insert_room_type(node.left, room_type, floor)
        elif floor > node.floor:
            node.right = self._insert_room_type(node.right, room_type, floor)

        return node

    def get_room_types_by_floor(self, floor, ac=True):
        if ac:
            return self._get_room_types_by_floor(self.root_ac, floor)
        else:
            return self._get_room_types_by_floor(self.root_non_ac, floor)

    def _get_room_types_by_floor(self, node, floor):
        result = []
        if node:
            if floor < node.floor:
                result.extend(self._get_room_types_by_floor(node.left, floor))
            elif floor > node.floor:
                result.extend(self._get_room_types_by_floor(node.right, floor))
            else:
                result.append(node.room_type)
                result.extend(self._get_room_types_by_floor(node.left, floor))
                result.extend(self._get_room_types_by_floor(node.right, floor))
        return result


if __name__ == '__main__':
    app = QApplication([])
    hotel_system = HotelManagementSystem()
    app.exec_()
