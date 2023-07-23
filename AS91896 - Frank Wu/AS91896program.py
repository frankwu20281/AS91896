from tkinter import * # The tkinter module is imported to create a visual GUI for the user to interact with
from tkinter import ttk, messagebox # From the tkinter module, the ttk module is imported to accesss tkinter's themed widget set, and also from tkinter module the messagebox function is imported to open messagebox's to display infomation
import json #The 'json' module is imported in order to effectively work with the saved_data.json file for saving reports.

class Main_window: # The Main_window class initiates the GUI part of the program and holds all the functions used in the program
    def __init__(self,master): 
        '''
        Description: When the Main_window class is run, the __init__ function will automatically run
        Args: None
        Returns: Creates a window on users device and displays all of the GUI elements on the main window
        '''
        global style , receipt_data_display, data , receipt_list# lets the variable "style" to be accessed anywhere in the program file, meaning it can be used/modified anywhere in the program code
        with open("storage.json") as file: # Opens the storage.json file and accesses the dictionary in the file
            data = json.load(file) 
            receipt_list = data["orders"] # Accesses the list of the orders key in the dictionary and stores it in receipt_list
        self.index = -1 if not receipt_list else 0  # Counter to keep count what receipt in the list the program currently is displaying/using, start at -1 because 0 is the item in list
        self.page_amount = len(receipt_list)    # Keep count of the total amount of receipts in the program 
        #configures the main window 
        root.title("Receipts") # Changes window title name to "Receipts"
        root.geometry("700x450") # Sets the main window size when the program first runs
        style = ttk.Style(root) # 
        style.theme_use("xpnative")
        self.theme = "Light"
        #Setting up all the styles for fonts/buttons/labels/entryboxes etc. 
        root.configure(bg= "SystemButtonFace") #Sets background colour of the program to be "SystemButtonFace"
        style.configure(root, font = ("Arial", 12), background = 'SystemButtonFace', foreground = "black") #Sets the default font to be Arial size 12 and the background of the font to be "SystemButtonFace" and the foreground of the font to be "black"
        
        style.configure("main.TFrame", font = (None, 12) , background = "#fbfbfb" ) # Sets the font of the of the frames using "main.TFrame" to be size 12, and setting the background colour to "#fbfbfb"
        style.configure("sub.TFrame", font = (None, 12) , background = "SystemButtonFace" ) # Sets the font of the of the frames using "sub.TFrame" to be size 12, and setting the background colour to "SystemButtonFace"

        style.configure('TButton', font = (None, 12), foreground = "Black")  # Sets the font of all buttons to be size 12 and the text colour to be black
        style.configure('TEntry', foreground = 'black')   # Sets the font of all the entry boxes text colour to be black
                  
        padding = {'padx':15, 'pady': 15} # Default external padding values for all of the frames
        
        #Creating menu bar
        menubar = Menu(root)
        root.config(menu=menubar)
        tool_menu = Menu(menubar, tearoff= 0)
        
        menubar.add_cascade(label="Tools", menu= tool_menu ) # Menubar named "Tools"
        tool_menu.add_command(label="Advanced Search", command= self.Search_window) # Adding a Advanced Search button to the menubar, when clicked it runs the Search_window function
        
        themes_submenu = Menu(tool_menu, tearoff= 0) # Adding a submenu to the menubar
        tool_menu.add_cascade(label="Themes", menu= themes_submenu) #Submemu named Themes
        themes_submenu.add_command(label= "Light" ,command= lambda :self.Themes("Light")) # Adding a Light button to the themes submenu, when clicked it changes the program to light theme 
        themes_submenu.add_command(label= "Dark" ,command= lambda :self.Themes("Dark")) # adding a Dark button to the themes submenu. when clicked it changes the program to dark theme
        
        tool_menu.add_separator() 
        
        reset_submenu = Menu(tool_menu, tearoff= 0) #Adding another submenu to the menubar
        tool_menu.add_cascade(label="Reset All", menu=reset_submenu ) #Submenu named Reset All
        reset_submenu.add_command(label = "Confirm", command = self.Reset) #When user clicks on Reset All it opens another button called comfirm, when user presses this button it runs the reset function
        
        tool_menu.add_separator()
        tool_menu.add_command(label= "Exit", command= self.Quit) #runs the Quit function when pressed
        #Program title and system theme button 
        ttk.Label(root, text= "Item Hire Tracker" ,  font= ("Arial", 20, 'bold')). pack (pady= 10)
        self.mode_button = ttk.Button(root, text= "Light theme", command= lambda :self.Themes("Dark" if self.theme == "Light" else "Light"))
        self.mode_button. pack(anchor= E, padx = 70,   expand= TRUE)
        #Creating 'master' frame to put all ui stuff in
        frame = ttk.Frame(root, style= "main.TFrame")
        frame.pack( padx= 20,pady= 10, expand= TRUE)
        #Frame with all the user entry ui 
        entry_frame=ttk.LabelFrame(frame, text= "Fill Out", style= "sub.TFrame")
        entry_frame.pack(side= LEFT, fill= BOTH, **padding) 
        #Label that asks user to input full name, and entrybox to let user input
        self.name_label = ttk.Label(entry_frame, text= "enter full name").grid(row=0, column=0, pady= 5, padx= 5)
        self.name_entry = ttk.Entry(entry_frame)
        self.name_entry.grid(row=0, column=1, pady= 5, padx= 5)
        #Label that asks user to input item name, and entrybox to let user input
        self.item_label = ttk.Label(entry_frame, text= "enter item name").grid(row=1, column= 0, pady= 5, padx= 5)
        self.item_entry = ttk.Entry(entry_frame)
        self.item_entry.grid(row=1, column=1, pady= 5, padx= 5)
        #Label that asks user to input item amount, and entrybox to let user input
        self.amount_label = ttk.Label(entry_frame, text= "enter item quantity").grid(row=2, column= 0, pady= 5, padx= 5)    
        self.amount_entry = ttk.Entry(entry_frame)
        self.amount_entry.grid (row=2, column=1, pady= 5, padx= 5)
        #Buy button that runs the Add function when pressed
        ttk.Button(entry_frame, text= "Add", command= lambda : self.Add(self.name_entry.get().strip().lower(),self.item_entry.get().strip().lower()
                , self.amount_entry.get().strip().lower()), style= "big.TButton").grid(row=3, column=1, pady= 5)
        #Return button that runs the Delete function when pressed
        ttk.Button(entry_frame, text = "Return", command = self.Delete).grid(row=3,column=0, pady= 5)
        # Frame with the receipt search bar 
        search_frame = ttk.LabelFrame(frame, text= "Search Receipt Number", style= "sub.TFrame")
        search_frame.pack(fill= X ,**padding)
        # Label and entrybox to let user search the receipts/orders by inputing receipt number
        ttk.Label(search_frame,text="Receipt:").pack(side=LEFT, padx= 5)
        self.search_entry = ttk.Entry(search_frame)
        # when user releases any key (eg. finishes typing) it will run the Receipt_number_search function
        self.search_entry.bind("<KeyRelease>", (lambda event: self.Receipt_number_search(self.search_entry.get())))
        self.search_entry.pack(side= LEFT, expand= TRUE, fill=X, padx = 5 , pady= 5)
        #Frame with the receipt display ui 
        display_frame=ttk.LabelFrame(frame, text= "Receipt Display", style= "sub.TFrame")
        display_frame.pack(**padding, expand=TRUE,fill = BOTH)
        
        #Label that displays the receipt data of the current receipt
        receipt_data_display = ttk.Label(display_frame, text="No receipts\n\n\n\n")
        receipt_data_display.pack( anchor= CENTER,expand= TRUE, pady= 5)
        #Button to open search window that displays the reciept data in a table format and has all search
        ttk.Button(display_frame, text= "Search All", command= self.Search_window).pack( anchor= CENTER,expand= TRUE, ipadx= 10)
        #Navagation buttons for user to change the currently displayed receipt data
        self.back = ttk.Button(display_frame, text="←", command= lambda  :self.Navagation_buttons("left"), state= DISABLED) #Go to next receipt data
        self.back.pack( side= LEFT, expand= TRUE ,anchor= CENTER, pady=10, padx= 5)
        self.page_number = ttk.Label(display_frame, text= f"{self.index+1} of {self.page_amount}") #The page number of the receipt that is currently being displayed
        self.page_number.pack(side= LEFT, expand= TRUE,  anchor= CENTER)
        self.forward = ttk.Button(display_frame, text= "→", command=lambda  : self.Navagation_buttons("right"), state= DISABLED) #Go to previous receipt data
        self.forward.pack( side= LEFT, expand= TRUE ,anchor= CENTER, pady=10, padx= 5)
        
        if receipt_list: #checks if program started with any preloaded infomation in the order list, and updates the program to show this info
            self.Receipt_shifting()
            
            
    def Search_window (self):  
        '''
        Description: Opens a new window that has the table view ui and the searchbar where you can search through all the data
        Args: None
        Returns: None
        '''
        global new_window, search_window_style #Globaling the varables new_window and search_window_style allowing them to be accessed throughout the program
        new_window = Toplevel(root)
        # Configuring the new window 
        new_window.title('Advanced Search') # Title of the new window
        new_window.configure(bg= "SystemButtonFace" if self.theme == "Light" else "#2b2b2b" ) #Setting background colour 
        search_window_style = ttk.Style(new_window) 
        search_window_style.theme_use("xpnative") # System style for the entryboxes, buttons and other ui that use ttk 
        search_window_style.configure("Treeview", foreground = "black") # Setting all of the text in the Treeview table to be black 
        search_window_style.configure("Treeview.Heading", foreground="black") # Setting text of the table heading to be black 
        self.sort_direction = True #Default sorting direction for all the columns 
        #Title and label for the window
        ttk.Label(new_window, text='Search All Receipts', font = ("Arial", 15, "bold") ).pack(pady= 10 )
        ttk.Label(new_window, text= 'Search for anything and click to display on main window:').pack()
        #Entry box for user to enter their search, binded to keyrelease so program will run search_choice function every time user stops typing  
        self.adv_search_entry = ttk.Entry(new_window)
        self.adv_search_entry.bind ("<KeyRelease>", lambda event: self.All_search( self.adv_search_entry.get().strip()))
        self.adv_search_entry.pack(padx= 10, fill= X)
        # Treeview table to display all of the programs stored receipt data, and scrollbar for the table 
        scrollbar = Scrollbar(new_window)
        
        self.tree_table = ttk.Treeview(new_window, columns=('Receipt', 'Name', 'Item', 'Quantity'), show = 'headings',yscrollcommand = scrollbar.set)
        self.tree_table.bind('<<TreeviewSelect>>', (lambda event: self.Double_click(self,self.tree_table.item(self.tree_table.selection()))))
        self.tree_table.pack(pady= 10, padx=10, fill= BOTH, expand= TRUE, side= LEFT)
        
        
        #First column for the table, Receipt number 
        self.tree_table.heading('Receipt', text = "Receipt Number", command= lambda: self.Sorting('Receipt', False if self.sort_direction  else True))
        self.tree_table.column('Receipt', anchor='center', minwidth=50)
        #Second column for the table, Full name 
        self.tree_table.heading('Name', text = "Full Name", command= lambda: self.Sorting('Name', False if self.sort_direction else True))
        self.tree_table.column('Name', anchor='center', minwidth=50)
        #Third column for the table, Item
        self.tree_table.heading('Item', text = "Item", command= lambda: self.Sorting('Item', False if self.sort_direction else True))
        self.tree_table.column('Item', anchor='center', minwidth=50)
        #Forth column for the table, Quantity
        self.tree_table.heading('Quantity', text = "Quantity", command= lambda: self.Sorting('Quantity', False if self.sort_direction else True))
        self.tree_table.column('Quantity', anchor='center', minwidth=50)
        # Putting the table onto the window    
        self.All_search(self.adv_search_entry.get().strip()) # Running the All_search function to populate the table with all the users data


    def Themes (self, theme ): 
        '''
        Description: Controls the colour scheme of the whole program, including the main window and any subwindows
        Args: theme : str (colour theme that the program is switching to )
        '''
        self.theme  = theme 
        self.mode_button.configure(text= "Dark Mode" if theme== "Dark" else "Light Mode") # Changes text on the theme button to display the current theme that is active 
        
        root.configure(bg= "#2b2b2b" if theme == "Dark" else 'SystemButtonFace') # Changes the main window background to match the current theme
        style.configure(root, font = ("Arial", 12), foreground = "white" if theme == "Dark" else 'black' 
                            ,background = "#2b2b2b" if theme == 'Dark' else "SystemButtonFace") #Changes the defualt text to match the current theme 
        style.configure("main.TFrame", font = (None, 12) , background = "#323232" if theme == 'Dark' else "#fbfbfb") #Changes the main frame to match the current theme 
        style.configure("sub.TFrame", font = (None, 12) , background = "#2b2b2b" if theme == 'Dark' else"SystemButtonFace"  ) #Changes the sub frame to match the current theme
        style.configure('TButton', font = (None, 12), foreground = "#262626"if theme == 'Dark' else "Black") #Changes the buttons to match the current theme 
        try: # Try function used to see if the search window is active because if it is not active if we try to configure the ui items on the non-opened window it will crash
            search_window_style.configure('TLabel', foreground= "black" if theme == "Light" else "white", 
              background= "SystemButtonFace" if theme== "Light" else "#2b2b2b") # Changes the search window text to match the current theme
            new_window.configure(bg= "SystemButtonFace" if theme == "Light" else "#2b2b2b" ) # Changes the search window background to match the current theme
        except: 
            pass 

    def Sorting (self, selected, sort_direction): 
        ''' 
        Description: When user clicks on the header of a column it will sort the currently displayed receipt data in an ascending/descending order according to that columns data
        Args: 
        selected : str (gets the name of the column heading that the user has clicked and wants to be sorted)
        sort_direction : Bool (the sorting direction is either true - reversed, or false - not reversed )
        '''
        self.sort_direction = sort_direction
        # Stores all of the currently displayed data of the column that was currently selected and its respective position on the table (repersented as a ID code) as a tuple that is stored in a list called "data"
        data = [(int(self.tree_table.set(child, selected))if selected == "Receipt" or selected == "Quantity" else (self.tree_table.set(child, selected) ), child) for child in self.tree_table.get_children('')]
        data.sort(reverse= sort_direction) # Sorts the data list depending on what sort_direction is
        for self.index, (value, child) in enumerate(data):self.tree_table.move(child,  '',self.index) #For every tuple in data, move the row assigned to the ID code to its new, sorted postion on the table
        for column in self.tree_table['columns']: # Adds an arrow next to the selected column that is currently selected to show what direction the data in that column has been sorted in(ascending/descending)
            if column != selected:self.tree_table.heading(column, text=column)
            else:
                arrow = '↑' if  sort_direction else '↓'
                self.tree_table.heading(column, text=f'{column} {arrow}')
        
    def All_search(self, typed):   
        '''
        Description: Lets user search for words that are in the currently displayed receipt data in the table 
        Args: typed : str (the text that the user has typed in the search bar)
        Returns: None
        '''  
        for row in self.tree_table.get_children(): self.tree_table.delete(row)           
        for search in receipt_list:  #seeing if user search matches anything in receipt list
            if typed == "":     #if user has typed nothing then display all receipts in listbox 
                self.tree_table. insert ('', END, values = (search['receipt'],search['name'].title(),search['item'].title(),search['quantity']))
            elif typed.lower() in str(search['receipt']) or typed.lower() in search['name'] or typed.lower() in search['item']or typed.lower() in search['quantity']:   # if user has typed something and it matches something in a receipt, display it in listbox
                self.tree_table. insert ('', END, values = (search['receipt'],search['name'].title(),search['item'].title(),search['quantity']))
        if not self.tree_table.get_children(0): self.tree_table. insert ('', END, values = ('No Results','-','-','-')) #if user search doesnt match anything, tell user there are no search results

    def Double_click (self, event ,selected_receipt): 
        '''
        Description: Updates main window to display the order that the user has selected in the advanced search window
        Args: event (var used in the lambda function that is used to run this function),  selected_receipt : dict (dictionary with the values of the receipt data that was selected in the table)
        '''
         #gets the string that the user has selected 
        self.index = next((self.index for (self.index, dict) in enumerate(receipt_list) if dict["receipt"] == selected_receipt['values'][0]), None) #searches for the dictionary that matches the receipt number, then finds the self.index of that dictionary in the receipt_list list
        self.Receipt_shifting() #updates the main window to display the order
    
    def Receipt_number_search (self, search_field ): #function to search for orders using receipt number
        '''
        Description: Searches the receipt data list for a receipt that matches the users input
        Args: search_field : str (the text that the user has typed into the search bar)
        Returns: None
        ''' 
        for dicts in receipt_list: # For every dictionary in the receipt_list list, it checks if the users receipt number input matches any of those dictionaries "receipt" value
            try: #Try converting user receipt number input into a interger, if user didnt input a interger the funciton wont run 
                search_field = int(search_field) 
            except ValueError: # If user has entered a phrase the searchbar text will turn red, indicating an error 
                self.search_entry.config(foreground= 'red')
                pass 
            else: #If user receipt number imput matches a value of "receipt" key in the dictionary, it finds the index of the dictionary in the receipt_list list and then runs the Receipt_shifting funciton to update the main window to display the order
                if search_field == dicts['receipt']: 
                    self.index = next((self.index for (self.index, dict) in enumerate(receipt_list) if dict["receipt"] == search_field), None)
                    self.search_entry.config(foreground= 'black')
                    self.Receipt_shifting() 
                    break
                else: # If the users input matches none of the receipts in the receipt_list, then change the searchbar's text to red to indicate an error to the user
                    self.search_entry.config(foreground= 'red')
        
                    
    def Receipt_shifting (self):
        '''
        Description: Uses the current value of self.index to update the main window receipt data display label to show the current receipt data by using the index to search receipt_list 
        for the data dictonary for that receipt/order
        Args: None 
        Returns: None
        '''
        receipt_order = receipt_list[self.index] #The dictionary of the order that is going to get displayed
        self.page_number.config(text= f"{self.index+1} of {self.page_amount}") #Updates the page number to show where the order is in the receipt_list
        #Updates the receipt_data_display Label on the main window to display the current order 
        receipt_data_display.config(text= f"Name: {receipt_order['name'].title()}\nReciept: #{str(receipt_order['receipt']).zfill(6)}\nItem: {receipt_order['item'].title()}\nQuantity: {receipt_order['quantity']}") 
        #Updates Navagation_buttons buttons according to the position of the displayed order in the receipt_list 
        self.forward.config(state= DISABLED if self.page_amount == 1 and self.index ==0 or self.index+1 == self.page_amount else ACTIVE)
        self.back.config(state= DISABLED if self.page_amount == 1 and self.index ==0  or self.index == 0 else ACTIVE)
        
    def Delete (self): 
        '''
        Description: Deletes the current order that is being displayed on the mainwindow from self.receipt_list
        Args: None 
        Returns: None
        ''' 
        try: #Deletes active order from receipt_list and from json file
            receipt_list.pop(self.index) 
            with open("storage.json", 'w') as file: json.dump(data, file, indent= 4)
        except IndexError: # If there is nothing in receipt_list this means theres no orders, meaning it will error
            messagebox.showerror("ERROR", "There are no receipts to return") # Messagebox to tell the user about the error
        else:
            self.page_amount -= 1 #Changes the index since the current receipt has been deleted, meaning the previous receipt should be displayed
        
            if self.index == self.page_amount: self.index -= 1 # If the deleted receipt is the last one, then index doesnt change since there is nothing before the first order 
            if self.page_amount == 0: # If after deleting the receipt, if there is no receipts left to display, change the label to "No Receipts"
                receipt_data_display.config(text= f"No Receipts\n\n\n\n")
                self.page_number.config(text = f"{self.index+1} of {self.page_amount}")
            else: # If after deleting there are still receipts to display, run the Receipt_shifting function to display the new receipt data
                self.Receipt_shifting()
                try: self.All_search( self.adv_search_entry.get().strip()) # If the advanced search window is open, update the table to remove the deleted receipt data
                except: pass      
    
    def Add(self, name, item, quantity): 
        '''
        Description: Checks if there are errors in users order input, if not then adds user's inputed data to the JSON file. If there are errors a error message window will open telling user about the error/s
        Args: name : str (the full name that the user has inputed), item : str (the item name that user has inputed), quantity : int (the item quantity that the user has inputed)
        Returns: None
        '''
        
        error_text= '' #Error text that will be displayed using the messagebox 
        
        if any(number.isdigit() for number in name) or not name: #Error checking for invalid name
            if error_text == '': error_text += " Name" #Adding name to the error text
            else: error_text += ", name " 
            self.name_entry.configure(foreground= "red") #Changing the text on the name entrybox to red to show user there is an error there
        if  any(number.isdigit() for number in item) or not item: #Error checking for invalid item name
            if error_text == '': error_text += " item name" #Adding item name to the error text
            else: error_text += ", item name" 
            
            self.item_entry.configure(foreground= "red") #Changing the text on the item entrybox to red to show user there is an error there
        if not quantity or not quantity.isdigit() or int(quantity)>500 or int(quantity)<1: #Error checking for invalid item quantity
            if error_text == '': error_text += "item quantity" #Adding item quantity to the error text
            else: error_text += ", item quantity (1-500)"
            self.amount_entry.configure(foreground= "red") #Changing the text on the quantity entrybox to red to show user there is an error there
        if error_text: #If there are any errors, then display a messagebox that tells the user where the errors are
            messagebox.showerror("Error", f"Invalid{error_text}")
            
        else: #If there aren't any errors, put the users data into a dictonary format and put that dictonary into the receipt_list
            data["receipt_numbers"] += 1  #Increasing the receipt_numbers value by one in the JSON file to not let receipts have the same receipt number
            receipt_list.append({"receipt": data["receipt_numbers"] , "name": name, "item": item, "quantity": quantity}) #Adding the data to receipt_list in a dictonary form
            self.page_amount += 1 #Increasing the page amount by one since we have added one receipt data to receipt_list
            self.index = 0 if self.index == -1 else self.page_amount - 1 #Changes the index to match where the newly added receipt data is placed in receipt_list
            self.name_entry.configure(foreground= "black"), self.item_entry.configure(foreground= "black"), self.amount_entry.configure(foreground= "black") #Changes all the entrybox text back to black since there are no errors
            with open("storage.json", 'w') as file: json.dump(data, file, indent= 4) #Adds the updated receipt_list and receipt_numbers to the JSON file
            self.name_entry.delete(0,END),self.item_entry.delete(0,END),self.amount_entry.delete(0,END) # Deletes the text in all of the entryboxes 
            self.Receipt_shifting() # Run the Receipt_shifting function to update the display window to show the newly added receipt data 
            try: self.All_search( self.adv_search_entry.get().strip()) # If advanced window is open, update the table to also show the newly added receipt data
            except: pass 
        
    def Navagation_buttons(self, button):  
        '''
        Description: Lets the user change the receipt that is being displayed on the main window by clicking on the left/right navagation buttons 
        Args: button : str (which way the user wants to shift the receipt data display)
        '''       
        if button == "left":  # If left button is clicked then shift index down one
            self.index -= 1 
        else: # If right button is clicked then shift index up one
            self.index += 1
        self.Receipt_shifting() # Updates the receipt data display to show the new receipt data
        
    def Reset (self):
        '''
        Description: Resets/deletes all the stored data on the JSON file 
        Args: None
        Returns: None
        '''
        data = {"orders": [], "receipt_numbers": 0} #Resets the data dictionary to its default, no data state 
        receipt_list = data['orders']  #Resets receipt_list so nothing is being stored
        self.index = -1 # Resets index
        self.page_amount = 0 #Resets page amount
        receipt_data_display.config(text= f"No receipts\n\n\n\n") #Since there is no data being stored, receipt data display will not be displaying an receipt data
        self.page_number.config(text = f"{self.index+1} of {self.page_amount}") #Reset page amount to be 0 of 0 
        with open("storage.json", 'w') as file: json.dump(data, file, indent= 4) #Removing all stored data in the JSON file
        
    def Quit (self):
        root.destroy()
root = Tk()   
program = Main_window(root)

root.mainloop()
