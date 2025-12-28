import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import ast
import sqlite3
import warnings

warnings.filterwarnings('ignore')


def execute_sqlite_query(query):
    try:
        # Connect to the SQLite database (or create it if not exists)
        connection = sqlite3.connect("rrsdb.db")
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(query)
        result = cursor.fetchall()

        # Commit the transaction and close the connection
        connection.commit()
        connection.close()

        return str(result)
    except sqlite3.Error as e:
        return f"Error executing query: {e}"


def center_window(root, width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


class DatabaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome Page")
        self.first_name_entry = None
        self.last_name_entry = None
        self.train_name_entry = None
        self.left_age_entry = None
        self.right_age_entry = None
        self.date_entry = None
        self.result_tree = None
        self.ssn_entry = None
        self.result_text = None

        # Add a label before the buttons
        welcome_label = Label(root, text="Welcome to the Railway Reservation System!", justify="center")
        welcome_label.grid(row=0, column=1, columnspan=3, padx=10, pady=5)

        query_label = Label(root,
                            text="Click on Query 1 to fetch the details of trains booked by passengers\n"
                                 "Click on Query 2 to fetch the details of passengers travelling on a particular date\n"
                                 "Click on Query 3 to fetch the details of passengers and their trains based on a "
                                 "given age range\n"
                                 "Click on Query 4 to fetch the details of Train names and number of passengers on it\n"
                                 "Click on Query 5 to fetch the details of all passengers travelling in a particular "
                                 "train\n"
                                 "Click on Query 6 to cancel tickets",
                            justify="left")
        query_label.grid(row=1, column=1, columnspan=3, padx=10, pady=5)

        # Create a button to execute the query
        query_1_button = Button(root, text="Query 1", command=self.name_query)
        query_1_button.grid(row=2, column=1, padx=10, pady=5, columnspan=1)

        # Create a button to execute the query
        query_2_button = Button(root, text="Query 2", command=self.date_query)
        query_2_button.grid(row=2, column=2, padx=10, pady=5, columnspan=1)

        # Create a button to execute the query
        query_3_button = Button(root, text="Query 3", command=self.age_query)
        query_3_button.grid(row=2, column=3, padx=10, pady=5, columnspan=1)

        # Create a button to execute the query
        query_4_button = Button(root, text="Query 4", command=self.train_count_query)
        query_4_button.grid(row=3, column=1, padx=10, pady=5, columnspan=1)

        # Create a button to execute the query
        query_5_button = Button(root, text="Query 5", command=self.train_name_query)
        query_5_button.grid(row=3, column=2, padx=10, pady=5, columnspan=1)

        # Create a button to execute the query
        query_6_button = Button(root, text="Query 6", command=self.update_query)
        query_6_button.grid(row=3, column=3, padx=10, pady=5, columnspan=1)

    def name_query(self):
        # Create labels and entry widgets for first and last names
        new_window = Toplevel(self.root)
        new_window.title('Query 1')

        fn_label = Label(new_window, text="First Name:", justify="center")
        fn_label.grid(row=0, column=0, padx=10, pady=5)

        self.first_name_entry = Entry(new_window, width=20)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=5)

        ln_label = Label(new_window, text="Last Name:", justify="center")
        ln_label.grid(row=1, column=0, padx=10, pady=5)

        self.last_name_entry = Entry(new_window, width=20)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=5)

        # Create a button to execute the query
        execute_button = Button(new_window, text="Search", command=self.execute_name_query)
        execute_button.grid(row=2, column=0, pady=10)

        # Create a button to clear the output
        clear_button = Button(new_window, text="Clear Output", command=self.clear_output)
        clear_button.grid(row=2, column=1, pady=10)

        # Create a Treeview widget to display the result
        columns = ("First Name", "Last Name", "Train Name", "Status")
        self.result_tree = ttk.Treeview(new_window, columns=columns, show="headings")
        for col in columns:
            self.result_tree.heading(col, text=col)
        self.result_tree.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

    def date_query(self):
        new_window = Toplevel(self.root)
        new_window.title('Query 2')

        date_label = Label(new_window, text="Train Date(yyyy-mm-dd):")
        date_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.date_entry = Entry(new_window, width=20)
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)

        # Create a button to execute the query
        execute_button = Button(new_window, text="Search", command=self.execute_date_query)
        execute_button.grid(row=2, column=0, pady=10)

        # Create a button to clear the output
        clear_button = Button(new_window, text="Clear Output", command=self.clear_output)
        clear_button.grid(row=2, column=1, pady=10)

        # Create a Treeview widget to display the result
        columns = ("First Name", "Last Name")
        self.result_tree = ttk.Treeview(new_window, columns=columns, show="headings")
        for col in columns:
            self.result_tree.heading(col, text=col)
        self.result_tree.grid(row=3, padx=10, pady=10, columnspan=2)

    def age_query(self):
        new_window = Toplevel(self.root)
        new_window.title('Query 3')

        age_label = Label(new_window, text="Display results for ages between:", justify="center")
        age_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.left_age_entry = Entry(new_window, width=20)
        self.left_age_entry.grid(row=1, column=0, padx=10, pady=5)

        self.right_age_entry = Entry(new_window, width=20)
        self.right_age_entry.grid(row=1, column=1, padx=10, pady=5)

        # Create a button to execute the query
        execute_button = Button(new_window, text="Search", command=self.execute_age_query)
        execute_button.grid(row=2, column=0, padx=10, pady=5)

        # Create a button to clear the output
        clear_button = Button(new_window, text="Clear Output", command=self.clear_output)
        clear_button.grid(row=2, column=1, padx=10, pady=5)

        # Create a Treeview widget to display the result
        columns = ("Train Number", "Train Name", "Source Station", "Destination Station",
                   "First Name", "Last Name", "Ticket Type", "Status")
        self.result_tree = ttk.Treeview(new_window, columns=columns, show="headings")
        for col in columns:
            self.result_tree.heading(col, text=col)
        self.result_tree.grid(row=3, padx=10, pady=10, columnspan=2)

    def train_count_query(self):
        new_window = Toplevel(self.root)
        new_window.title('Query 4')

        count_label = Label(new_window, text="Fetch details of all trains running and number of passengers:")
        count_label.grid(row=0, column=0, padx=10, pady=5, columnspan=2)

        # Create a button to execute the query
        execute_button = Button(new_window, text="Search", command=self.execute_train_count_query)
        execute_button.grid(row=2, column=0, pady=10)

        # Create a button to clear the output
        clear_button = Button(new_window, text="Clear Output", command=self.clear_output)
        clear_button.grid(row=2, column=1, pady=10)

        # Create a Treeview widget to display the result
        columns = ("Train Name", "Count of Passengers")
        self.result_tree = ttk.Treeview(new_window, columns=columns, show="headings")
        for col in columns:
            self.result_tree.heading(col, text=col)
        self.result_tree.grid(row=3, padx=10, pady=10, columnspan=2)

    def train_name_query(self):
        new_window = Toplevel(self.root)
        new_window.title('Query 5')

        train_name_label = Label(new_window, text="Train Name:")
        train_name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.train_name_entry = Entry(new_window, width=20)
        self.train_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Create a button to execute the query
        execute_button = Button(new_window, text="Search", command=self.execute_train_name_query)
        execute_button.grid(row=1, column=0, pady=10)

        # Create a button to clear the output
        clear_button = Button(new_window, text="Clear Output", command=self.clear_output)
        clear_button.grid(row=1, column=1, pady=10)

        # Create a Treeview widget to display the result
        columns = ("First Name", "Last Name")
        self.result_tree = ttk.Treeview(new_window, columns=columns, show="headings")
        for col in columns:
            self.result_tree.heading(col, text=col)
        self.result_tree.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

    def update_query(self):
        new_window = Toplevel(self.root)
        new_window.title('Query 6')

        ssn_label = Label(new_window, text="Enter Passenger SSN:")
        ssn_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.ssn_entry = Entry(new_window, width=20)
        self.ssn_entry.grid(row=0, column=1, padx=10, pady=5)

        # Create a button to execute the query
        execute_button = Button(new_window, text="Cancel Ticket", command=self.execute_update_query)
        execute_button.grid(row=1, column=0, pady=10)

        # Create a button to clear the output
        clear_button = Button(new_window, text="Clear Output", command=self.clear_update_output)
        clear_button.grid(row=1, column=1, pady=10)

        # Create a text widget to display the result
        self.result_text = tk.Text(new_window, height=10, width=70)
        self.result_text.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
        self.result_text.insert(tk.END, "Results will be displayed here.")

    def execute_name_query(self):
        # Get the first and last names from the entries
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()

        # Formulate and execute the SQL query
        query = f'''SELECT P.FirstName,P.LastName, T.TrainName, B.Status
                    FROM Passenger AS P 
                    JOIN Booked AS B ON P.SSN=B.PassengerSSN
                    JOIN Train AS T ON B.TrainNumber = T.TrainNumber
                    WHERE B.Status='Booked' AND P.FirstName='{first_name}' AND P.LastName='{last_name}';'''
        result = ast.literal_eval(execute_sqlite_query(query))

        # Display the result in the Treeview widget
        if len(result) > 0:
            self.display_result(result)
        else:
            messagebox.showerror("Error", f'No ticket booked for - {first_name} {last_name}')

    def execute_date_query(self):
        # Get the first and last names from the entries
        date = self.date_entry.get()
        query = f'''SELECT P.FirstName,P.LastName
                    FROM Passenger P
                    JOIN Booked B ON P.SSN = B.PassengerSSN
                    JOIN Train T ON B.TrainNumber = T.TrainNumber
                    JOIN TrainStatus TS ON T.TrainName=TS.TrainName
                    WHERE TS.TrainDate='{date}' AND B.Status = 'Booked';'''

        result = ast.literal_eval(execute_sqlite_query(query))

        # Display the result in the Treeview widget
        if len(result) > 0:
            self.display_result(result)
        else:
            messagebox.showerror("Error", f'No passenger has booked a Train on {date}')

    def execute_age_query(self):
        # Get the first and last names from the entries
        left_year = self.left_age_entry.get()
        right_year = self.right_age_entry.get()
        query = f'''SELECT Train.TrainNumber, Train.TrainName, Train.SourceStation, Train.DestinationStation,
                    Passenger.FirstName, Passenger.LastName, Booked.TicketType, Booked.Status
                    FROM Passenger
                    JOIN Booked ON Passenger.SSN = Booked.PassengerSSN
                    JOIN Train ON Booked.TrainNumber = Train.TrainNumber
                    WHERE strftime('%Y', 'now') - strftime('%Y', Passenger.BirthDate) BETWEEN {left_year} AND
                    {right_year}'''

        result = ast.literal_eval(execute_sqlite_query(query))

        # Display the result in the Treeview widget
        if len(result) > 0:
            self.display_result(result)
        else:
            messagebox.showerror("Error", f'No passenger lies in the age range of {left_year} and {right_year}')

    def execute_train_count_query(self):
        query = ''' SELECT t.TrainName, COUNT(b.TrainNumber) AS passenger_count
                    FROM Train t LEFT JOIN Booked b ON t.TrainNumber = b.TrainNumber
                    WHERE b.Status='Booked'
                    GROUP BY t.TrainName;'''

        result = ast.literal_eval(execute_sqlite_query(query))

        # Display the result in the Treeview widget
        self.display_result(result)

    def execute_train_name_query(self):
        name = self.train_name_entry.get()

        query = f'''SELECT p.FirstName,p.LastName
                    FROM Passenger p 
                    JOIN Booked b ON p.SSN = b.PassengerSSN
                    JOIN Train t ON b.TrainNumber = t.TrainNumber
                    WHERE  t.TrainName = '{name}' AND b.Status = 'Booked';'''

        result = ast.literal_eval(execute_sqlite_query(query))

        # Display the result in the Treeview widget
        if len(result) > 0:
            self.display_result(result)
        else:
            messagebox.showerror("Error", f"There is no passenger booked on the train '{name}'")

    def execute_update_query(self):
        ssn = int(self.ssn_entry.get())
        # Connect to Database
        conn = sqlite3.connect('rrsdb.db')

        # Implement query logic
        cursor = conn.cursor()

        # Retrieve the ticket details before deletion for later use
        query_select = f'''SELECT TrainNumber, TicketType, Status
                           FROM Booked
                           WHERE PassengerSSN = {ssn};'''
        cursor.execute(query_select)
        ticket_details = cursor.fetchone()

        # Delete the record
        query_delete = f'''
            DELETE FROM Booked
            WHERE PassengerSSN = {ssn}
        '''
        cursor.execute(query_delete)
        conn.commit()

        # Check if there are passengers in the waiting list for the same train
        if ticket_details and ticket_details[2] == 'Booked':
            query_waiting_list = f'''
                SELECT PassengerSSN
                FROM Booked
                WHERE TrainNumber = {ticket_details[0]} AND Status = 'WaitL'
                LIMIT 1
            '''
            cursor.execute(query_waiting_list)
            waiting_passenger = cursor.fetchone()

            # If there is a passenger in the waiting list, update their status to 'Confirmed'
            if waiting_passenger:
                query_update_waiting = f'''
                    UPDATE Booked
                    SET Status = 'Booked'
                    WHERE PassengerSSN = {waiting_passenger[0]}
                '''
                cursor.execute(query_update_waiting)
                conn.commit()
                result = (f"Passenger {ssn} ticket cancelled. Passenger {waiting_passenger[0]} changed ticket status "
                          f"to booked")
            else:
                result = f"No passenger in waiting list. Cancelled passenger {ssn}'s ticket."
        else:
            result = f"No passenger has a ticket booked with SSN={ssn}"

        # Display the result in the text widget
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

    def display_result(self, result):
        # Clear previous items in the Treeview
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        # Insert new data into the Treeview
        for row in result:
            self.result_tree.insert("", "end", values=row)

    def clear_output(self):
        # Clear the Treeview widget
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

    def clear_update_output(self):
        # Clear the result text
        self.result_text.delete(1.0, tk.END)


if __name__ == "__main__":
    master = tk.Tk()
    center_window(master, 600, 250)
    app = DatabaseGUI(master)
    master.mainloop()
