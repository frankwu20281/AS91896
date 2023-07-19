from tkinter import * # The tkinter module is imported to create a visual GUI for the user to interact with
from tkinter import ttk, messagebox # From the tkinter module, the ttk module is imported to accesss tkinter's themed widget set, and also from tkinter module the messagebox function is imported to open messagebox's to display infomation
import json #The 'json' module is imported in order to effectively work with the saved_data.json file for saving reports.

class Main_window: # The Main_window class initiates the GUI part of the program and holds all the functions used in the program
    def __init__(self, master): 
        '''
        Description: When the Main_window class is run, the __init__ function will automatically run
        Args: None 
        Returns: Creates a window on users device and displays all of the GUI elements on the main window
        '''
        global style , receipt_data_display# lets the variable "style" to be accessed anywhere in the program file, meaning it can be used/modified anywhere in the program code
        with open("storage.json") as file: # Opens the storage.json file and accesses the dictionary in the file
            self.data = json.load(file) 
            self.receipt_list = self.data["orders"] # Accesses the list of the orders key in the dictionary and stores it in self.receipt_list
        self.index = -1 if not self.receipt_list else 0  # Counter to keep count what receipt in the list the program currently is displaying/using, start at -1 because 0 is the item in list
        self.page_amount = len(self.receipt_list)    # Keep count of the total amount of receipts in the program 
        #configures the main window 
        root.title("Receipts") # Changes window title name to "Receipts"
        root.geometry("700x450") # Sets the main window size when the program first runs
        style = ttk.Style(root) # 
        style.theme_use("xpnative")
        self.mode = "Light"
        #Setting up all the styles for fonts/buttons/labels/entryboxes etc. 
        root.configure(bg= "SystemButtonFace") #Sets background colour of the program to be "SystemButtonFace"
        style.configure(root, font = ("Arial", 12), background = 'SystemButtonFace', foreground = "black") #Sets the default font to be Arial size 12 and the background of the font to be "SystemButtonFace" and the foreground of the font to be "black"
        
        style.configure("main.TFrame", font = (None, 12) , background = "#fbfbfb" ) # Sets the font of the of the frames using "main.TFrame" to be size 12, and setting the background colour to "#fbfbfb"
        style.configure("sub.TFrame", font = (None, 12) , background = "SystemButtonFace" ) # Sets the font of the of the frames using "sub.TFrame" to be size 12, and setting the background colour to "SystemButtonFace"

        style.configure('TButton', font = (None, 12), foreground = "Black")  # Sets the font of all buttons to be size 12 and the text colour to be black
        style.configure('TEntry', foreground = 'black')   # Sets the font of all the entry boxes text colour to be black
                  
        padding = {'padx':15, 'pady': 15} # Default external padding values for all of the frames
        
        #Creating menu bar
        menubar = Menu(master)
        master.config(menu=menubar)
        tool_menu = Menu(menubar, tearoff= 0)
        
        menubar.add_cascade(label="Tools", menu= tool_menu ) # Menubar named "Tools"
        tool_menu.add_command(label="Advanced Search", command= self.Search_window) # Adding a Advanced Search button to the menubar, when clicked it runs the Search_window function
        
        themes_submenu = Menu(tool_menu, tearoff= 0) # Adding a submenu to the menubar
        tool_menu.add_cascade(label="Themes", menu= themes_submenu) #Submemu named Themes
        themes_submenu.add_command(label= "Light" ,command= lambda :self.Themes("Light")) # Adding a Light button to the themes submenu, when clicked it changes the program to light mode 
        themes_submenu.add_command(label= "Dark" ,command= lambda :self.Themes("Dark")) # adding a Dark button to the themes submenu. when clicked it changes the program to dark mode
        
        tool_menu.add_separator() 
        
        reset_submenu = Menu(tool_menu, tearoff= 0) #Adding another submenu to the menubar
        tool_menu.add_cascade(label="Reset All", menu=reset_submenu ) #Submenu named Reset All
        reset_submenu.add_command(label = "Confirm", command = self.Reset) #When user clicks on Reset All it opens another button called comfirm, when user presses this button it runs the reset function
        
        tool_menu.add_separator()
        tool_menu.add_command(label= "Exit", command= self.Quit) #runs the Quit function when pressed
        #Program title and system mode button 
        ttk.Label(root, text= "Item Hire Tracker" ,  font= ("Arial", 20, 'bold')). pack (pady= 10)
        self.mode_button = ttk.Button(root, text= "Light mode", command= lambda :self.Themes("Dark" if self.mode == "Light" else "Light"))
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
        self.amount_label = ttk.Label(entry_frame, text= "enter item amount").grid(row=2, column= 0, pady= 5, padx= 5)    
        self.amount_entry = ttk.Entry(entry_frame)
        self.amount_entry.grid (row=2, column=1, pady= 5, padx= 5)
        #Buy button that runs the Add function when pressed
        ttk.Button(entry_frame, text= "Buy", command= lambda : self.Add(self.name_entry.get().strip().lower(),self.item_entry.get().strip().lower()
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
        
        if self.receipt_list: #checks if program started with any preloaded infomation in the order list, and updates the program to show this info
            self.Receipt_shifting()
            
            
    def Search_window (self):  
    
        global new_window, search_window_style
        new_window = Toplevel(root)
        new_window.title('Advanced Search')
        new_window.configure(bg= "SystemButtonFace" if self.mode == "Light" else "#2b2b2b" )
        search_window_style = ttk.Style(new_window)
        search_window_style.theme_use("xpnative")
        search_window_style.configure("Treeview", foreground = "black")
        search_window_style.configure("Treeview.Heading", foreground="black")
        self.sort_direction = True
        #Title and label for the window
        ttk.Label(new_window, text='Search In All Receipts', font = ("Arial", 15, "bold") ).pack(pady= 10 )
        ttk.Label(new_window, text= 'Search for anything and click to display on main window:').pack()

        #entry box for user to enter their search, binded to keyrelease so program will run search_choice function every time user stops typing  
        self.adv_search_entry = ttk.Entry(new_window)
        self.adv_search_entry.bind ("<KeyRelease>", lambda event: self.All_search( self.adv_search_entry.get().strip()))
        self.adv_search_entry.pack(padx= 10, fill= X)
        
        columns= ('Receipt', 'Name', 'Item', 'Amount')
        
        scrollbar = Scrollbar(new_window)
        self.tree_table = ttk.Treeview(new_window, columns=columns, show = 'headings',yscrollcommand = scrollbar.set)
        scrollbar.config(command = self.tree_table.yview)
        scrollbar.pack(side= RIGHT, fill= Y, pady= 10)
        
        self.tree_table.heading('Receipt', text = "Receipt number", command= lambda: self.Sorting('Receipt', False if self.sort_direction  else True))
        self.tree_table.column('Receipt', anchor='center', minwidth=50)
        
        self.tree_table.heading('Name', text = "Full Name", command= lambda: self.Sorting('Name', False if self.sort_direction else True))
        self.tree_table.column('Name', anchor='center', minwidth=50)
        
        self.tree_table.heading('Item', text = "Item", command= lambda: self.Sorting('Item', False if self.sort_direction else True))
        self.tree_table.column('Item', anchor='center', minwidth=50)
        
        self.tree_table.heading('Amount', text = "Amount", command= lambda: self.Sorting('Amount', False if self.sort_direction else True))
        self.tree_table.column('Amount', anchor='center', minwidth=50)
        
        self.tree_table.pack(pady= 10, padx=10, fill= BOTH, expand= TRUE, side= LEFT)
        
        
        
        #listbox to show users search se "white")
        self.tree_table.bind('<<TreeviewSelect>>', (lambda event: self.Double_click(self,self.tree_table.item(self.tree_table.selection()))))
        
        
        self.All_search(self.adv_search_entry.get().strip())


    def Themes (self, mode ): #function to control colour theme of the whole program
        self.mode  = mode
        self.mode_button.configure(text= "Dark Mode" if self.mode == "Dark" else "Light Mode")
        
        root.configure(bg= "#2b2b2b" if mode == "Dark" else 'SystemButtonFace')
        style.configure(root, font = ("Arial", 12), foreground = "white" if mode == "Dark" else 'black' 
                            ,background = "#2b2b2b" if mode == 'Dark' else "SystemButtonFace")
        

        style.configure("main.TFrame", font = (None, 12) , background = "#323232" if mode == 'Dark' else "#fbfbfb")
        style.configure("sub.TFrame", font = (None, 12) , background = "#2b2b2b" if mode == 'Dark' else"SystemButtonFace"  )

        style.configure('TButton', font = (None, 12), foreground = "#262626"if mode == 'Dark' else "Black")

        try: 
            search_window_style.configure('TLabel', foreground= "black" if self.mode == "Light" else "white", 
              background= "SystemButtonFace" if self.mode == "Light" else "#2b2b2b")
            new_window.configure(bg= "SystemButtonFace" if self.mode == "Light" else "#2b2b2b" )
            

        except: 
            pass 

    def Sorting (self, selected, sort_direction): 
        self.sort_direction = sort_direction
        data = [(int(self.tree_table.set(child, selected))if selected == "Receipt" or selected == "Amount" else (self.tree_table.set(child, selected) ), child) for child in self.tree_table.get_children('')]
        data.sort(reverse= sort_direction)
        for index, (value, child) in enumerate(data):self.tree_table.move(child, '', index)
        for column in self.tree_table['columns']:
            if column != selected:self.tree_table.heading(column, text=column)
            else:
                arrow = '↑' if  sort_direction else '↓'
                self.tree_table.heading(column, text=f'{column} {arrow}')
        
    def All_search(self, typed):   #search all function for the advanced search window    
        for row in self.tree_table.get_children(): self.tree_table.delete(row)           
        for search in self.receipt_list:  #seeing if user search matches anything in receipt list
            if typed == "":     #if user has typed nothing then display all receipts in listbox 
                self.tree_table. insert ('', END, values = (search['receipt'],search['name'].title(),search['item'].title(),search['amount']))
            elif typed.lower() in str(search['receipt']) or typed.lower() in search['name'] or typed.lower() in search['item']or typed.lower() in search['amount']:   # if user has typed something and it matches something in a receipt, display it in listbox
                self.tree_table. insert ('', END, values = (search['receipt'],search['name'].title(),search['item'].title(),search['amount']))
        if not self.tree_table.get_children(0): self.tree_table. insert ('', END, values = ('No Results','-','-','')) #if user search doesnt match anything, tell user there are no search results

    def Double_click (self, event,selected_receipt): #updates main window to display the order that the user has selected in the advanced search window
         #gets the string that the user has selected 
        
        self.index = next((index for (index, dict) in enumerate(self.receipt_list) if dict["receipt"] == selected_receipt['values'][0]), None) #searches for the dictionary that matches the receipt number, then finds the index of that dictionary in the self.receipt_list list
        self.Receipt_shifting() #updates the main window to display the order
    
    def Receipt_number_search (self, search_field ): #function to search for orders using receipt number 
        for dicts in self.receipt_list: # for every dictionary in the self.receipt_list list, it checks if the users receipt number input matches any of those dictionaries "receipt" value

        
            try: #try converting user receipt number input into a interger, if user didnt input a interger the funciton wont run 
                search_field = int(search_field) 
            except ValueError:
                pass 
            else: #if user receipt number imput matches a value of "receipt" key in the dictionary, it finds the index of the dictionary in the self.receipt_list list and then runs the Receipt_shifting funciton to update the main window to display the order
                if search_field == dicts['receipt']: 
                    self.index = next((index for (index, dict) in enumerate(self.receipt_list) if dict["receipt"] == search_field), None)
                    self.Receipt_shifting()
                    
    def Receipt_shifting (self): #funtion that updates the main window to display the order
     
        receipt_order = self.receipt_list[self.index] #the dictionary of the order that is going to get displayed

        self.page_number.config(text= f"{self.index+1} of {self.page_amount}") #updates the page number to show where the order is in the total stored orders

        
        #updates the receipt_data_display Label on the main window to display the current order 
        receipt_data_display.config(text= f"Name: {receipt_order['name'].title()}\nReciept: {str(receipt_order['receipt']).zfill(6)}\nItem: {receipt_order['item'].title()}\nAmount: {receipt_order['amount']}") 
        
        #updates Navagation_buttons buttons according to the position of the displayed order in the self.receipt_list 
        self.forward.config(state= DISABLED if self.page_amount == 1 and self.index ==0 or self.index+1 == self.page_amount else ACTIVE)
        self.back.config(state= DISABLED if self.page_amount == 1 and self.index ==0  or self.index == 0 else ACTIVE)
        
    def Delete (self): #Deletes active order being displayed on main window  
        try: #Deletes active order from self.receipt_list and from json file
            self.receipt_list.pop(self.index) 
            self.Write_json()
  
        except IndexError: # if there is nothing in self.receipt_list this means theres no orders, meaning it will error
            messagebox.showerror("ERROR", "There are no receipts to return")
        else:
            self.page_amount -= 1 
            
            if self.index == self.page_amount: self.index -= 1 
            
            if self.page_amount == 0: 
                receipt_data_display.config(text= f"No receipts\n\n\n\n")
                self.page_number.config(text = f"{self.index+1} of {self.page_amount}")
            else:
                self.Receipt_shifting()
                try: self.All_search( self.adv_search_entry.get().strip())
                except: pass      
    
    def Add(self, name, item, amount): # checks for errors in user order input and then adds the order dictionary to the json file 

        error_text = [] 
        self.data["receipts"] += 1 
        receipt_number =self.data["receipts"]
        if any(number.isdigit() for number in name) or not name:self.name_entry.configure(foreground= "red"), error_text.append("name") #error checking for invalid name
        if  any(number.isdigit() for number in item) or not item: self.item_entry.configure(foreground= "red"), error_text.append("item") #error checking for invalid item 
        if not amount or not amount.isdigit() or int(amount)>500 or int(amount)<1: self.amount_entry.configure(foreground= "red"), error_text.append("item-amount(1-500)") #error chekcing for invalid item    
        if error_text: messagebox.showerror("Error", f"Invalid { ', '.join(map(str, error_text))}")
        else: 
            self.receipt_list.append({"receipt": receipt_number, "name": name, "item": item, "amount": amount})
            self.page_amount += 1
            self.index = 0 if self.index == -1 else self.page_amount -1
            self.name_entry.configure(foreground= "black"), self.item_entry.configure(foreground= "black"), self.amount_entry.configure(foreground= "black")
            self.Receipt_shifting()
            self.Write_json()
            try: self.All_search( self.adv_search_entry.get().strip())
            except: pass 
            
    def Write_json(self):
        with open("storage.json", 'w') as file: json.dump(self.data, file, indent= 4)
            
    def Navagation_buttons(self, button):         
        if button == "left": self.index -= 1 
        else: self.index += 1
        self.Receipt_shifting()
        
    def Reset (self):
        self.data = {"orders": [], "receipts": 0}
        self.receipt_list = []
        self.index = -1
        self.page_amount = 0
        receipt_data_display.config(text= f"No receipts\n\n\n\n")
        self.page_number.config(text = f"{self.index+1} of {self.page_amount}")
        self.Write_json()
        
    
    def Quit (self):
        root.destroy()
root = Tk()   
program = Main_window(root)

root.mainloop()
