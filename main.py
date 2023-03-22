from tkinter import *
from tkinter import messagebox
import random
import ration_sql_connection

'''
Ma'am for your info:
the program is divided into 4 main functions that separately into the admin and distributor functions

this main python file calls the python file: ration_sql_connection for the sql connectivity parts
'''

root = Tk()
root.title('Ration Management System')

# main window
heading = Label(root, text='Welcome to our ration management system!\nPlease select an option:')
heading.grid(row=0, column=0, columnspan=3)


# functions called by the frames
def open_admin_window():
    admin = Toplevel()
    admin.title('Admin Page')

    def open_register_frame():
        lst = []

        # check the card type and also the if else condition and how the data is stored

        def open_enter_register_frame(frame):
            enter_register_frame = LabelFrame(frame, padx=50, pady=50)
            enter_register_frame.grid(row=1, column=0, padx=10, pady=10)

            def click():

                name = (e_name.get()).strip()
                aadhaar = (e_aadhaar.get()).strip()
                income = (e_total_income.get()).strip()
                family = (e_family.get()).strip()
                card_type = ''

                check = True
                if len(name) == 0 or len(aadhaar) != 12:
                    check = False
                if not aadhaar.isdigit() or not income.isdigit() or not family.isdigit():
                    check = False
                if not check:
                    convey_info_label.config(text='Please enter the correct details')

                elif ration_sql_connection.in_use_sql(aadhaar_no=aadhaar):
                    convey_info_label.config(text='The aadhaar number is already in use')

                else:
                    enter_register_frame.destroy()
                    income_per_person = abs(int(income) // int(family))
                    if 0 <= income_per_person < 300000:
                        card_type = 'BPL'
                    else:
                        card_type = 'APL'

                lst.append([name, aadhaar, income, family, card_type])

            # defining the entries and corresponding buttons
            e_name_label = Label(enter_register_frame, text='Enter your full name:')
            e_name = Entry(enter_register_frame, width=75)
            e_aadhaar_label = Label(enter_register_frame, text='Enter your aadhaar number:')
            e_aadhaar = Entry(enter_register_frame, width=75)
            e_total_income_label = Label(enter_register_frame, text='Enter the total income:')
            e_total_income = Entry(enter_register_frame, width=75)
            e_family_label = Label(enter_register_frame, text='Enter the number of people in the family:')
            e_family = Entry(enter_register_frame, width=75)
            convey_info_label = Label(enter_register_frame, text='Please enter the details:')
            submit_button = Button(enter_register_frame, text='Enter', command=click)

            # the signup grid system
            e_name_label.grid(row=0, column=0, columnspan=3)
            e_name.grid(row=1, column=0, columnspan=3)
            e_aadhaar_label.grid(row=2, column=0, columnspan=3)
            e_aadhaar.grid(row=3, column=0, columnspan=3)
            e_total_income_label.grid(row=4, column=0, columnspan=3)
            e_total_income.grid(row=5, column=0, columnspan=3)
            e_family_label.grid(row=6, column=0, columnspan=3)
            e_family.grid(row=7, column=0, columnspan=3)
            convey_info_label.grid(row=8, column=0, columnspan=3)
            submit_button.grid(row=9, column=0, columnspan=3, padx=10)

        register_frame = LabelFrame(admin, padx=50, pady=50)
        register_frame.grid(row=1, column=0, padx=10, pady=10)

        generate_frame = LabelFrame(register_frame, padx=50, pady=50)
        generate_frame.grid(row=1, column=0, padx=10, pady=10)

        open_enter_register_frame(register_frame)

        def click(rationnumber):
            password1 = (e_password.get()).strip()
            password2 = (e_confirm_password.get()).strip()
            # print(password1,password2)
            if password1 != password2:
                convey_info_label.config(text='Passwords do not match')

            else:
                lst.append([rationnumber, password1])
                lst[0], lst[1] = lst[1], lst[0]
                # now lst contains [[ration_no, password],[name, aadhaar, income, family, card_type]]
                # print(lst)
                ration_sql_connection.register_records_sql(lst)
                ration_sql_connection.register_user_info(lst[0][0], lst[1][4])
                messagebox.showinfo('FYI', 'Your records have been registered')
                register_frame.destroy()

        def generate_ration_number():
            number = 0
            while True:
                number = random.randint(10 ** 9, 10 ** 10 - 1)
                # checks if this number is already in the tables as a ration number
                check = ration_sql_connection.in_use_sql(ration_no=number)
                # if its not used check = False
                # check = False
                if not check:
                    break
            return number

        ration_number = generate_ration_number()
        # creating the widgets
        ration_label = Label(generate_frame, text=f'Your ration number is {ration_number}')
        password_label = Label(generate_frame, text='Enter password')
        e_password = Entry(generate_frame, width=50, show='*')
        confirm_password_label = Label(generate_frame, text='Confirm password')
        e_confirm_password = Entry(generate_frame, width=50, show='*')
        convey_info_label = Label(generate_frame, text='REMEMBER YOUR PASSWORD')
        submit_button = Button(generate_frame, text='Enter', command=lambda: click(ration_number))

        # the sub grid system
        ration_label.grid(row=0, column=0, columnspan=3)
        password_label.grid(row=1, column=0, columnspan=3)
        e_password.grid(row=2, column=0, columnspan=3)
        confirm_password_label.grid(row=3, column=0, columnspan=3)
        e_confirm_password.grid(row=4, column=0, columnspan=3)
        convey_info_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
        submit_button.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    def open_edit_frame():
        # lst = [[0, 0], []]  # lst right now contains useless values to help access the list's elements later
        lst = []

        def open_enter_edit_frame(frame):
            enter_edit_frame = LabelFrame(frame, padx=50, pady=50)
            enter_edit_frame.grid(row=1, column=0, padx=10, pady=10)

            def delete():
                ration_sql_connection.delete_record_sql(lst[0][0])
                # rishabh delete all records of this ration number from the tables
                messagebox.showinfo('FYI', 'Your info has been deleted')
                edit_frame.destroy()

            def click():

                name = (e_name.get()).strip()
                aadhaar = (e_aadhaar.get()).strip()
                income = (e_total_income.get()).strip()
                family = (e_family.get()).strip()
                card_type = ''

                check = True
                if len(name) == 0 or len(aadhaar) != 12:
                    check = False
                if not aadhaar.isdigit() or not income.isdigit() or not family.isdigit():
                    check = False
                if not check:
                    convey_info_label.config(text='Please enter the correct details')

                elif ration_sql_connection.in_use_sql(aadhaar_no=aadhaar):
                    convey_info_label.config(text='The aadhaar number is already in use')

                else:
                    edit_frame.destroy()
                    messagebox.showinfo('FYI', 'Your info has been updated')
                    income_per_person = abs(int(income) // int(family))
                    if 0 <= income_per_person < 300000:
                        card_type = 'BPL'
                    else:
                        card_type = 'APL'

                    # lst[1] = [name, aadhaar, income, family, card_type]
                    lst.append([name, aadhaar, income, family, card_type])
                    # the lst is: [[ration_no, password], the new [name, aadhaar, income, family, card_type]]
                    ration_sql_connection.edit_records_sql(lst)
                    ration_sql_connection.edit_user_ration_sql(lst[0][0], lst[1][4])
                    # print(lst)

            # lst_of_info = ration_sql_connection.fill_entry_for_edit(int(lst[0][0]))  # gets the old details

            # defining the entries and corresponding buttons
            e_name_label = Label(enter_edit_frame, text='Enter your full name:')
            e_name = Entry(enter_edit_frame, width=75)
            # e_name.insert(0, lst_of_info[2])

            e_aadhaar_label = Label(enter_edit_frame, text='Enter your aadhaar number:')
            e_aadhaar = Entry(enter_edit_frame, width=75)
            # e_aadhaar.insert(0, lst_of_info[3])

            e_total_income_label = Label(enter_edit_frame, text='Enter the total income:')
            e_total_income = Entry(enter_edit_frame, width=75)
            # e_total_income.insert(0, lst_of_info[4])

            e_family_label = Label(enter_edit_frame, text='Enter the number of people in the family:')
            e_family = Entry(enter_edit_frame, width=75)
            # e_family.insert(0, lst_of_info[5])

            convey_info_label = Label(enter_edit_frame, text='Please enter the details:')
            submit_button = Button(enter_edit_frame, text='Submit', command=click)
            delete_button = Button(enter_edit_frame, text='Delete', command=delete)

            # the signup grid system
            e_name_label.grid(row=0, column=0, columnspan=3)
            e_name.grid(row=1, column=0, columnspan=3)
            e_aadhaar_label.grid(row=2, column=0, columnspan=3)
            e_aadhaar.grid(row=3, column=0, columnspan=3)
            e_total_income_label.grid(row=4, column=0, columnspan=3)
            e_total_income.grid(row=5, column=0, columnspan=3)
            e_family_label.grid(row=6, column=0, columnspan=3)
            e_family.grid(row=7, column=0, columnspan=3)
            convey_info_label.grid(row=8, column=0, columnspan=3)
            submit_button.grid(row=9, column=1)
            delete_button.grid(row=9, column=2)

        edit_frame = LabelFrame(admin, padx=20, pady=20)
        edit_frame.grid(row=1, column=1, padx=10, pady=10)
        open_enter_edit_frame(edit_frame)
        # enter_rn_frame is pasted over the frame where we edit our details
        # enter_rn_frame is used to get the ration no and password and authenticate it
        # rn is ration number
        enter_rn_frame = LabelFrame(edit_frame, padx=100, pady=60)
        enter_rn_frame.grid(row=1, column=0, padx=10, pady=10)

        def value_entry():
            a, b = e1.get(), e2.get()
            torf = ration_sql_connection.check_info_sql(ration_number=a, user_password=b)
            # print(torf)
            if torf:
                # lst[0] = [a, b]
                # print(lst)
                lst.append([a, b])

                enter_rn_frame.destroy()
            else:
                convey_info_label.config(text='Details do not match')

        # creating all the buttons and entry widgets
        e1_label = Label(enter_rn_frame, text='Enter ration number')
        e1 = Entry(enter_rn_frame, width=50)
        e2_label = Label(enter_rn_frame, text='Enter password')
        e2 = Entry(enter_rn_frame, width=50, show='*')
        convey_info_label = Label(enter_rn_frame, text='')
        enter_button = Button(enter_rn_frame, text="Enter", padx=10, pady=10, command=value_entry)
        # grid system
        e1_label.grid(row=0, column=0)
        e1.grid(row=1, column=0)
        e2_label.grid(row=2, column=0)
        e2.grid(row=3, column=0)
        convey_info_label.grid(row=4, column=0)
        enter_button.grid(row=5, column=0)

    # creating buttons
    b_register = Button(admin, text="Register", padx=40, pady=20, borderwidth=5, command=open_register_frame)
    b_edit = Button(admin, text="Edit", padx=40, pady=20, borderwidth=5, command=open_edit_frame)

    # the sub grid system
    b_register.grid(row=0, column=0, padx=10, pady=10)
    b_edit.grid(row=0, column=1, padx=10, pady=10)


def open_user_window(ration_number):
    user = Toplevel()
    user.title('User Page')

    ration_number = int(ration_number)
    ration_sql_connection.update_user_info_date(ration_number)
    # update_user_info(ration_number ) .... this updates the month,year in the list and if its new, updates balance kgs

    lst = ration_sql_connection.get_user_records_sql(ration_number)
    # in order(ration_number,card_type,list of names, list of cost, list of balance)
    # get_user_records(ration_number) .... this returns a list of [name, card_type, lst_items, lst_cost, lst_number]
    # print(lst, 'line 265 main')
    name = lst[0]
    ration_card_type = lst[1]
    lst_items = lst[2]
    lst_cost = lst[3]  # the cost
    lst_number = lst[4]  # the amt of kgs remaining
    total_cost = 0
    print(lst_items, lst_number, lst_cost, sep='\n')
    # creating and placing the first few labels
    l1 = Label(user, text=f'Welcome {name}(Ration number:{ration_number})').grid(row=0, column=0, padx=5, pady=5)
    l2 = Label(user, text=f'Card type: {ration_card_type}').grid(row=1, column=0, padx=5, pady=5)

    lst_entries = []
    # creating a frame to print all the data:
    user_frame = LabelFrame(user)
    user_frame.grid(row=2, column=0, padx=10, pady=10)

    def update_max_that_can_be_bought():
        lst_entries.clear()
        for i in range(len(lst_items)):
            item_string = f'{lst_items[i]},max {lst_number[i]} units ({lst_cost[i]} rupees)'
            item_label = Label(user_frame, text=item_string).grid(row=i, column=0)
            my_entry = Entry(user_frame)
            my_entry.grid(row=i, column=1, pady=5, padx=10)
            lst_entries.append(my_entry)

    def calculate(entry_list, lst_num):
        # entry list contains a list of the amount he wants
        # lst_num is a list of the maximum ration he can buy
        # this function calculates the cost of the ration
        # and updates the max units the person can buy now in the tables

        nonlocal total_cost, lst_cost
        new_cost = 0
        convey_info_label.config(text='')
        for i in range(len(entry_list)):
            lst_num[i] = int(lst_num[i]) - int(entry_list[i])  # does this list number refer to the og one?
            new_cost += int(entry_list[i]) * int(lst_cost[i])
        # print(lst_num, 'line 290 main')
        ration_sql_connection.update_user_info_ration(lst_num, ration_number)  # updates the max possible he can buy

        total_cost += new_cost
        cost_label.config(text=f'The total cost is {total_cost}')
        update_max_that_can_be_bought()

    # issues when i enter -ve numbers
    def submit(lst_num):
        entry_list = []  # this list collects all the entered info
        entry_list.clear()

        for entries in lst_entries:
            entry_list.append(str(entries.get()))

        # now, checking if the entered data is valid
        torf = True
        for i in entry_list:
            try:
                int(i)
                if int(i) < 0:
                    # print('less than 0')
                    torf = False
            except ValueError:
                torf = False

        if not torf:
            # print('yare yare')
            convey_info_label.config(text='Please enter the correct data(+ve integers)')
            torf = True

        for i in range(len(entry_list)):

            if int(entry_list[i]) > int(lst_number[i]):
                torf = False
        if not torf:
            convey_info_label.config(text='Maximum limit exceeded')
            torf = True

        else:  # the entered data is good to go
            calculate(entry_list, lst_num)

    for i in range(len(lst_items)):
        item_string = f'{lst_items[i]},max {lst_number[i]} units ({lst_cost[i]} rupees)'
        item_label = Label(user_frame, text=item_string).grid(row=i, column=0)
        my_entry = Entry(user_frame)
        my_entry.grid(row=i, column=1, pady=5, padx=10)
        lst_entries.append(my_entry)

    # creating buttons and labels
    convey_info_label = Label(user_frame, text='')
    submit_button = Button(user_frame, text='Enter', command=lambda: submit(lst_number))
    cost_label = Label(user_frame, text='')
    # placing it in the grid
    convey_info_label.grid(row=len(lst_items), column=0, columnspan=3, padx=10, pady=10)
    submit_button.grid(row=len(lst_items) + 1, column=0, columnspan=3, padx=10, pady=10)
    cost_label.grid(row=len(lst_items) + 2, column=0, columnspan=3, padx=10, pady=10)


# functions called by the main buttons
def open_admin_frame():
    # admin_window_is_open = False

    def value_entry():
        torf = ration_sql_connection.check_info_sql(admin_id=e1.get(), admin_password=e2.get())
        # print(torf)
        if torf:
            '''global admin_window_is_open
            if not admin_window_is_open:
                open_admin_window()
                admin_window_is_open = True'''
            open_admin_window()
            convey_info_label.config(text='Details authenticated')
        else:
            convey_info_label.config(text='Details do not match')

    admin_frame = LabelFrame(root, padx=15, pady=10)
    admin_frame.grid(row=2, column=0, padx=10, pady=10)

    # creating all the buttons and entry widgets
    e1_label = Label(admin_frame, text='Enter admin code')
    e1 = Entry(admin_frame, width=50)
    e2_label = Label(admin_frame, text='Enter admin password')
    e2 = Entry(admin_frame, width=50, show='*')
    convey_info_label = Label(admin_frame, text='')
    enter_button = Button(admin_frame, text="Enter", padx=10, pady=10, command=value_entry)

    # grid system
    e1_label.grid(row=0, column=0)
    e1.grid(row=1, column=0)
    e2_label.grid(row=2, column=0)
    e2.grid(row=3, column=0)
    convey_info_label.grid(row=4, column=0)
    enter_button.grid(row=5, column=0)


def open_distributor_frame():
    def value_entry():
        a, b = e1.get(), e2.get()
        torf = ration_sql_connection.check_info_sql(ration_number=a, user_password=b)
        if torf:
            open_user_window(a)
            convey_info_label.config(text='Details authenticated')
        else:
            convey_info_label.config(text='Details do not match')

    distributor_frame = LabelFrame(root, padx=15, pady=10)
    distributor_frame.grid(row=2, column=1, padx=10, pady=10)

    # creating all the buttons and entry widgets
    e1_label = Label(distributor_frame, text='Enter ration number')
    e1 = Entry(distributor_frame, width=50)
    e2_label = Label(distributor_frame, text='Enter password')
    e2 = Entry(distributor_frame, width=50, show='*')
    convey_info_label = Label(distributor_frame, text='')
    enter_button = Button(distributor_frame, text="Enter", padx=10, pady=10, command=value_entry)

    # grid system
    e1_label.grid(row=0, column=0)
    e1.grid(row=1, column=0)
    e2_label.grid(row=2, column=0)
    e2.grid(row=3, column=0)
    convey_info_label.grid(row=4, column=0)
    enter_button.grid(row=5, column=0)


# creating buttons
b_admin = Button(root, text="Admin", padx=40, pady=20, borderwidth=5, command=open_admin_frame)
b_distributor = Button(root, text="Distributor", padx=40, pady=20, borderwidth=5, command=open_distributor_frame)

# the main grid system
b_admin.grid(row=1, column=0, padx=10, pady=10)
b_distributor.grid(row=1, column=1, padx=10, pady=10)


def complete_close():

    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


root.protocol('WM_DELETE_WINDOW', complete_close)
root.mainloop()
