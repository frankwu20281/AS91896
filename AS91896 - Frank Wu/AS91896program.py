from tkinter import * 
from tkinter import ttk, messagebox
from random import randint
import json

class MainWindow: 
    def __init__(self, master):
        with open("storage.json") as file:
            self.data = json.load(file)
            print(self.data)
            self.receipt_list = self.data["orders"]
            file.close()
        print(self.receipt_list)
        self.index = -1 if not self.receipt_list else 0  #counter to keep count what receipt in the list the program currently is displaying/using, start at -1 because 0 is the item in list
        self.page_amount = 0 if not self.receipt_list else len(self.receipt_list)    #keep count of the total amount of receipts in the program 
        
        #config the program window
        self.master = master 
        root.title("Receipts")
        root.geometry("700x400")
        self.style = ttk.Style(root)
        self.style.theme_use("xpnative")
        
        self.mode = "Light"
        root.configure(bg= "SystemButtonFace")
        self.style.configure(root, font = ("Arial", 12), background = 'SystemButtonFace', foreground = "black")
        

        self.style.configure("main.TFrame", font = (None, 12) , background = "#fbfbfb" )
        self.style.configure("sub.TFrame", font = (None, 12) , background = "SystemButtonFace" )

        self.style.configure('TButton', font = (None, 12), foreground = "Black") 
        self.style.configure('TEntry', foreground = 'black')     
    
        

        ipadding = {'ipadx':40, 'ipady': 40}
        padding = {'padx':15, 'pady': 15}
        

        #creating menu bar
        menubar = Menu(master)
        master.config(menu=menubar)
        tool_menu = Menu(menubar, tearoff= 0)
        
        menubar.add_cascade(label="Tools", menu= tool_menu )
        tool_menu.add_command(label="Advanced Search", command= self.search_window)
        
        themes_submenu = Menu(tool_menu, tearoff= 0)
        tool_menu.add_cascade(label="Themes", menu= themes_submenu)
        themes_submenu.add_command(label= "Light" ,command= lambda :self.themes("Light")) #SystemButtonFace for default colour
        themes_submenu.add_command(label= "Dark" ,command= lambda :self.themes("Dark"))
        
        tool_menu.add_separator()
        
        reset_submenu = Menu(tool_menu, tearoff= 0)
        tool_menu.add_cascade(label="Reset All", menu=reset_submenu )
        reset_submenu.add_command(label = "Confirm", command = self.reset)
        
        tool_menu.add_separator()
        tool_menu.add_command(label= "Exit", command= self.quit)
        
        #program title and system mode button 
        ttk.Label(root, text= "Item Hire Tracker" ,  font= ("Arial", 20, 'bold')). pack (pady= 10)
        self.mode_button = ttk.Button(root, text= "Light mode", command= lambda :self.themes("Dark" if self.mode == "Light" else "Light"))
        self.mode_button. pack(anchor= E, padx = 70,   expand= TRUE)
        
        #creating 'master' frame to put all ui stuff in
        
        frame = ttk.Frame(root, style= "main.TFrame")
        frame.pack( padx= 20,pady= 10, expand= TRUE)
        
        #frame with all the user entry stuff 
        self.EntryFrame=ttk.LabelFrame(frame, text= "fill out", style= "sub.TFrame")
        self.EntryFrame.pack(side= LEFT, fill= BOTH, **padding) 

        self.name_label = ttk.Label(self.EntryFrame, text= "enter full name").grid(row=0, column=0, pady= 5, padx= 5)
        self.name_entry = ttk.Entry(self.EntryFrame)
        self.name_entry.grid(row=0, column=1, pady= 5, padx= 5)

        self.item_label = ttk.Label(self.EntryFrame, text= "enter item name").grid(row=1, column= 0, pady= 5, padx= 5)
        self.item_entry = ttk.Entry(self.EntryFrame)
        self.item_entry.grid(row=1, column=1, pady= 5, padx= 5)

        self.amount_label = ttk.Label(self.EntryFrame, text= "enter item amount").grid(row=2, column= 0, pady= 5, padx= 5)    
        self.amount_entry = ttk.Entry(self.EntryFrame)
        self.amount_entry.grid (row=2, column=1, pady= 5, padx= 5)

        ttk.Button(self.EntryFrame, text= "Buy", command= lambda : self.add(self.name_entry.get().strip().lower(),self.item_entry.get().strip().lower()
                , self.amount_entry.get().strip().lower()), style= "big.TButton").grid(row=3, column=0, pady= 5)
        
        
        ttk.Button(self.EntryFrame, text = "Return", command = self.delete).grid(row=3,column=1, pady= 5)

        # frame with the receipt search bar 
        SearchFrame = ttk.LabelFrame(frame, text= "Search Receipt Number", style= "sub.TFrame")
        SearchFrame.pack(fill= X ,**padding)
        
        self.search_entry = ttk.Entry(SearchFrame)
        self.search_entry.bind("<KeyRelease>", (lambda event: self.receipt_number_search(self.search_entry.get())))
        self.search_entry.pack(side= LEFT, expand= True, padx = 5)
        
        ttk.Button(SearchFrame, text= "Search All", command= self.search_window).pack(side= LEFT ,padx=5, pady = 5)
   
        
        #frame with the receipt display stuff 
        DisplayFrame=ttk.LabelFrame(frame, text= "Receipt", style= "sub.TFrame")
        DisplayFrame.pack(**padding, expand=TRUE,fill = BOTH)

        self.receipt_image = ttk.Label(DisplayFrame, text="No receipts\n\n\n\n")
        self.receipt_image.pack( anchor= CENTER,expand= TRUE)

        self.back = ttk.Button(DisplayFrame, text="←", command= lambda  :self.nav("left"), state= DISABLED)
        self.back.pack( side= LEFT, expand= TRUE ,anchor= CENTER, pady=10)

        self.page_number = ttk.Label(DisplayFrame, text= f"{self.index+1} of {self.page_amount}")
        self.page_number.pack(side= LEFT, expand= TRUE,  anchor= CENTER)
        
        self.forward = ttk.Button(DisplayFrame, text= "→", command=lambda  : self.nav("right"), state= DISABLED)
        self.forward.pack( side= LEFT, expand= TRUE ,anchor= CENTER, pady=10)
        
        if self.receipt_list:
            
            self.receipt_shifting()
            
            
    def search_window (self):   #function to initiate advanced search window 
        #window config stuff
        
        SearchWindow = Toplevel(root)
        SearchWindow.title('Advanced Search')
        SearchWindow.configure(bg= "SystemButtonFace" if self.mode == "Light" else "#2b2b2b" )
        style = ttk.Style(SearchWindow)
        style.theme_use("xpnative")
        style.configure("TCombobox", foreground = "black")

        Label(SearchWindow, text='Search In All Receipts', font = ("Arial", 15, "bold"), foreground= "black" if self.mode == "Light" else "white", 
              background="SystemButtonFace" if self.mode == "Light" else "#2b2b2b" ).pack(pady= 10 )
        Label(SearchWindow, text= 'Double click to select:').pack()

        #entry box for user to enter their search, binded to keyrelease so program will run search_choice function every time user stops typing  
        self.adv_search_entry = ttk.Entry(SearchWindow)
        self.adv_search_entry.bind ("<KeyRelease>", lambda event: self.all_search( self.adv_search_entry.get().strip()))
     
        self.adv_search_entry.pack(padx= 10, fill= X)
        #listbox to show users search results, when user double clicks on option it displays it on main window
        self.receipt_storage = Listbox(SearchWindow, width= 50, background= "SystemButtonFace" if self.mode == "Light" else "#2b2b2b", 
                                       foreground= "black" if self.mode == "Light" else "white")
        self.receipt_storage.bind('<Double-Button>', (lambda event: self.double_click(self)))
        self.receipt_storage.pack(pady= 10, padx=10, fill= BOTH, expand= TRUE, side= LEFT)
        
        self.all_search(self.adv_search_entry.get().strip())


    def themes (self, mode ): #function to control colour theme of the whole program

        print(self.mode)
        self.mode  = mode
        self.mode_button.configure(text= "Dark Mode" if self.mode == "Dark" else "Light Mode")
        
        root.configure(bg= "#2b2b2b" if mode == "Dark" else 'SystemButtonFace')
        self.style.configure(root, font = ("Arial", 12), foreground = "white" if mode == "Dark" else 'black' 
                            ,background = "#2b2b2b" if mode == 'Dark' else "SystemButtonFace")
        

        self.style.configure("main.TFrame", font = (None, 12) , background = "#323232" if mode == 'Dark' else "#fbfbfb")
        self.style.configure("sub.TFrame", font = (None, 12) , background = "#2b2b2b" if mode == 'Dark' else"SystemButtonFace"  )

        self.style.configure('TButton', font = (None, 12), foreground = "#262626"if mode == 'Dark' else "Black")


    def all_search(self, typed):   #search all function for the advanced search window    
        print('allsearchstart')
        search_list =[] 
        self.receipt_storage.delete(0, END)
        for dicts in self.receipt_list: 
            print(dicts, "- receipt list")
            item_text = f"Name: {dicts['name'].title()} - Receipt: {dicts['receipt']} - Item: {dicts['item'].title()} - Amount: {dicts['amount']}"
            search_list.append(item_text)   #add receipt list to receipt display listbox
            
        for search in search_list:  #seeing if user search matches anything in receipt list
            if typed == "":     #if user has typed nothing then display all receipts in listbox 
                self.receipt_storage.insert(END, search)
            elif typed.lower() in search.lower():   # if user has typed something and it matches something in a receipt, display it in listbox
                self.receipt_storage.insert(END, search)
        if not self.receipt_storage.get(0): #if user search doesnt match anything, tell user there are no search results
            print('no')
            self.receipt_storage.insert(END, "No Search Results")  
            
    def receipt_number_search (self, search_field ):
        for dicts in self.receipt_list:
             #get the receipt number (key), and receipt list (value of key)
            print (dicts, '-receipt list')
            try: 
                search_field = int(search_field)
            except ValueError:
                pass 
            else: 
                if search_field == dicts['receipt']: 
                    self.index = next((index for (index, dict) in enumerate(self.receipt_list) if dict["receipt"] == search_field), None)
                    self.receipt_shifting()
            
    def double_click (self, event):
        selected_receipt = self.receipt_storage.get(self.receipt_storage.curselection())
        receipt_number = int(selected_receipt[selected_receipt.find("Receipt")+9: selected_receipt.find("Item")-3].strip())
        print (receipt_number)
        self.index = next((index for (index, dict) in enumerate(self.receipt_list) if dict["receipt"] == receipt_number), None)
        self.receipt_shifting()
    
    def receipt_shifting (self):
        
        
        
        receipt_order = self.receipt_list[self.index]
        
        
        self.page_number.config(text= f"{self.index+1} of {self.page_amount}")
        print(receipt_order, "receipt list", self.index, " index")
        print(self.receipt_list)
        

        self.receipt_image.config(text= f"Store \nName: {receipt_order['name'].title()}\nReciept: {str(receipt_order['receipt']).zfill(6)}\nItem: {receipt_order['item'].title()}\nAmount: {receipt_order['amount']}")
        
        self.forward.config(state= DISABLED if self.page_amount == 1 and self.index ==0 or self.index+1 == self.page_amount else ACTIVE)
        self.back.config(state= DISABLED if self.page_amount == 1 and self.index ==0  or self.index == 0 else ACTIVE)
        
    def delete (self):
        print(self.index)
        try:
            self.receipt_list.pop(self.index)
            self.write_json()
  
        except IndexError: 
            messagebox.showerror("ERROR", "There are no receipts to return")
        else:
            
           
            self.page_amount -= 1 
            
            if self.index == self.page_amount:
                self.index -= 1 
            if self.page_amount == 0: 
                self.receipt_image.config(text= f"No receipts\n\n\n\n")
                self.page_number.config(text = f"{self.index+1} of {self.page_amount}")
            else:
                self.receipt_shifting()
                try:
                    self.all_search( self.adv_search_entry.get().strip())
                except: 
                    pass 
                
                
            
    
    def add(self, name, item, amount): 

        error_text = [] 
        self.data["receipts"] += 1 
        receipt_number =self.data["receipts"]
        if any(number.isdigit() for number in name) or not name:
            self.name_entry.configure(foreground= "red")
            error_text.append("name")
        if  any(number.isdigit() for number in item) or not item:
            self.item_entry.configure(foreground= "red")
            error_text.append("item")
        if not amount or not amount.isdigit() or int(amount)>500 or int(amount)<1:
            self.amount_entry.configure(foreground= "red")
            error_text.append("item-amount(1-500)")     
        if error_text:        
            messagebox.showerror("Error", f"Invalid { ', '.join(map(str, error_text))}")
        else:
            
            self.receipt_list.append({"receipt": receipt_number, "name": name, "item": item, "amount": amount})
            print(self.receipt_list)
            print(self.data)
            self.page_amount += 1
            self.index = 0 if self.index == -1 else self.page_amount -1
            self.receipt_shifting()
            self.name_entry.configure(foreground= "black"), self.amount_entry.configure(foreground= "black"), self.item_entry.configure(foreground= "black")
            self.write_json()
            
    def write_json(self):
        with open("storage.json", 'w') as file:
            json.dump(self.data, file, indent= 4)
            file.close()
            print('json done')
            
    def nav(self, button):         
        if button == "left":
            self.index -= 1 
        else:
            self.index += 1
        
        self.receipt_shifting()
        
    def reset (self):
        self.data = {"orders": [], "receipts": 0}
        self.receipt_list = []
        self.index = -1
        self.page_amount = 0
        self.receipt_image.config(text= f"No receipts\n\n\n\n")
        self.page_number.config(text = f"{self.index+1} of {self.page_amount}")
        self.write_json()
        
    
    
    def quit (self):
        root.destroy()
root = Tk()   
program = MainWindow(root)

root.mainloop()
