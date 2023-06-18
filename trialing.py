from tkinter import * 
from tkinter import messagebox


class MainWindow: 
    
    receipt_list = []   #list to store receipt
    receipt_dict ={}    #dictionary to store receipt data using receipt number as key 
    index = -1          #counter to keep count what receipt in the list the program currently is displaying/using, start at -1 because 0 is the item in list
    page_amount = 0     #keep count of the total amount of receipts in the program 
    def __init__(self, master):
    
        #config the program window
        self.master = master 
        root.title("Receipts")
        root.geometry("700x300")

        self.search_window_active = False
        self.theme_colour ='SystemButtonFace'

        #creating menu bar
        menubar = Menu(master)
        master.config(menu=menubar)
        tool_menu = Menu(menubar, tearoff= 0)
        menubar.add_cascade(label="Tools", menu= tool_menu )
        
        tool_menu.add_command(label="Advanced Search", command= self.search_window)
        
        
        themes_submenu = Menu(tool_menu, tearoff= 0)
        themes_submenu.add_command(label= "Light" ,command= lambda :self.themes("SystemButtonFace")) #SystemButtonFace for default colour
    
        themes_submenu.add_command(label= "Dark" ,command= lambda :self.themes("Black"))
        tool_menu.add_cascade(label="Themes", menu= themes_submenu)
        
        tool_menu.add_separator()
        tool_menu.add_command(label= "Exit", command= self.quit)
        
        #creating 'master' frame to put all ui stuff in
        frame = Frame(root)
        frame.pack( )

        Label(root,text='Store').pack( anchor=N)
        
        
        #frame with all the user entry stuff 
        EntryFrame=LabelFrame(frame, text= "fill out")
        EntryFrame.pack(side= LEFT, fill= BOTH) 

        self.name_label = Label(EntryFrame, text= "enter full name")
        self.name_label.grid(row=0, column=0)
        self.name_entry = Entry(EntryFrame)
        self.name_entry.grid(row=0, column=1)


        self.receipt_label = Label(EntryFrame, text = "enter receipt number")
        self.receipt_label.grid(row= 1, column= 0)
        self.receipt_entry = Entry(EntryFrame)
        self.receipt_entry.grid(row=1, column=1 )

        self.item_label = Label(EntryFrame, text= "enter item name")
        self.item_label.grid(row=2, column= 0)
        self.item_entry = Entry(EntryFrame)
        self.item_entry.grid(row=2, column=1)

        self.amount_label = Label(EntryFrame, text= "enter item amount")
        self.amount_label.grid(row=3, column= 0)
        self.amount_entry = Spinbox(EntryFrame, from_ = 1,to = 500)
        self.amount_entry. grid (row=3, column=1)

        Button(EntryFrame, text= "Buy", command= self.add).grid(row=5, column=0)
        Button(EntryFrame, text = "Return", command = self.delete).grid(row=5,column=1)
       
        

        # frame with the receipt search bar 
        SearchFrame = LabelFrame(frame, text= "Receipt Search")
        SearchFrame.pack(fill= X)

        
        self.search_entry = Entry(SearchFrame)
        self.search_entry.bind("<KeyRelease>", (lambda event: self.receipt_search(self)))
        self.search_entry.pack(side= LEFT, fill= X, expand= True)
        
        Button(SearchFrame, text= "Advanced Search Menu", command= self.search_window).pack(side= LEFT)
        
        
        
        #frame with the receipt display stuff 
        DisplayFrame=LabelFrame(frame, text= "Receipt")
        DisplayFrame.pack( fill=  BOTH, expand= TRUE)

        self.receipt_image = Label(DisplayFrame, text="No receipts\n\n\n\n")
        self.receipt_image.pack(fill= X)

        self.back = Button(DisplayFrame, text="<-", command= self.previous_receipt, state= DISABLED)
        self.back.pack(side= LEFT)

        self.page_number = Label(DisplayFrame, text= f"{MainWindow.index+1} of {MainWindow.page_amount}")
        self.page_number.pack(side= LEFT,fill= BOTH, expand= True)
        
        self.forward = Button(DisplayFrame, text= "->", command= self.next_receipt, state= DISABLED)
        self.forward.pack(side= LEFT)
        
        
    def themes (self, colour ):
        
        
        
        root.config(bg= colour)
        self.theme_colour = colour 
            
  
    def search_window (self):
        self.search_window_active = True
        SearchWindow = Toplevel(root)
        
        SearchWindow.title('Advanced Search')
        
        SearchWindow.config(bg= self.theme_colour)
        
        Label(SearchWindow, text='Advanced Search').pack()
        self.dropdown= StringVar()
        self.dropdown.set("Select Search type")
        
        self.dropdown_menu= OptionMenu(SearchWindow, self.dropdown, "Receipt", "Name", "Item", "Search All", command= self.search_choice)
        
        self.dropdown_menu.pack()

        self.adv_search_entry = Entry(SearchWindow)
        self.adv_search_entry.bind ("<KeyRelease>", lambda event: self.search_choice(self))
        self.adv_search_entry.pack(padx= 5, fill= X)

        self.receipt_storage = Listbox(SearchWindow, width= 50)
        self.receipt_storage.bind('<Double-Button>', (lambda event: self.double_click(self)))
        #self.search_entry.bind("<Return>", (lambda event: self.adv_search(self)))
        self.receipt_storage.pack(pady= 5, padx=5, fill= X, anchor= S)
    


    def search_choice(self, event):
        
        
        self.receipt_storage.delete(0, END)
        choice = self.dropdown.get()
    
        if choice == "Name":
            MainWindow.name_search(self, event)
        elif choice =="Receipt":
            MainWindow.receipt_search(self, event) 
        elif choice == "Item":
            MainWindow.item_search(self, event)
        elif choice == "Search All":
            
            MainWindow.all_search(self, event)

    def all_search(self, event):
        print('start')
        self.search_list =[]
        typed = self.adv_search_entry.get()
        
        for receipt_number, receipt_list in MainWindow.receipt_dict.items():
            
            print(receipt_list, "yes")
            item_text = f"Name: {receipt_list[0]} - Receipt: {receipt_number} - Item: {receipt_list[1]} - Amount: {receipt_list[2]}"
            self.search_list.append(item_text)
        
            
        
        for search in self.search_list:
            if typed == "":
                self.receipt_storage.insert(END, search)
            elif typed.lower() in search.lower():
                self.receipt_storage.insert(END, search)
        else:
            self.receipt_storage.insert(END, "No Search Results")
                
            
       
            
            
        print ('done')
        

    def name_search(self, event):
        name = self.adv_search_entry.get().strip()
        
        

        
        for receipt_number, receipt_list in MainWindow.receipt_dict.items():
            print (list)
            if list[0] == name:
                
                
                MainWindow.index = MainWindow.receipt_list.index(receipt_number)
                self.page_number.config(text = f"{MainWindow.index+1} of {MainWindow.page_amount}")                                
                self.page_number.config(text= f"{MainWindow.index+1} of {MainWindow.page_amount}")
                print(MainWindow.receipt_dict[receipt_number], "yes")
                item_text = f"Name: {receipt_list[0]} - Receipt: {receipt_number} - Item: {receipt_list[1]} - Amount: {receipt_list[2]}"
                self.receipt_storage.insert(END, item_text)
        else:
            print('no')
            self.receipt_storage.insert(END, "No Search Results")
        
        ###if inlist == False:
            ###messagebox.showerror("error", "receipts with this name not found")###
    
    def item_search(self, event):
        item = self.adv_search_entry.get().strip()
        self.receipt_storage.delete(0, END)


        
        for receipt_number, receipt_list in MainWindow.receipt_dict.items():
            print (list)
            if list[1] == item:

                
                MainWindow.index = MainWindow.receipt_list.index(receipt_number)
                self.page_number.config(text = f"{MainWindow.index+1} of {MainWindow.page_amount}")                                
                self.page_number.config(text= f"{MainWindow.index+1} of {MainWindow.page_amount}")
                print(MainWindow.receipt_dict[receipt_number], "yes")
                item_text = f"Name: {receipt_list[0]} - Receipt: {receipt_number} - Item: {receipt_list[1]} - Amount: {receipt_list[2]}"
                self.receipt_storage.insert(END, item_text)
        
        else:
            self.receipt_storage.insert(END, "No Search Results")        
        #if inlist == False:
            #messagebox.showerror("error", "receipts with this item not found")
        

    def receipt_search (self,event):
        
        if self.search_window_active == True:
            receipt_number = self.adv_search_entry.get()
        else:
            receipt_number = self.search_entry.get()
        if receipt_number in MainWindow.receipt_list: 
            
            self.receipt_shifting(receipt_number)
            if self.search_window_active == True: 

                item_text = f"Name: {MainWindow.receipt_dict[receipt_number][0]} - Receipt: {receipt_number} - Item: {MainWindow.receipt_dict[receipt_number][1]} Amount: {MainWindow.receipt_dict[receipt_number][2]}"
                self.receipt_storage.insert(END, item_text)
        else:
            self.receipt_storage.insert(END, "No Search Results")
        #else: 
            #messagebox.showerror("error", "receipt not found")
            
    def double_click (self, event):
        selected_receipt = self.receipt_storage.get(self.receipt_storage.curselection())
        
        
       
        receipt_number = selected_receipt[selected_receipt.find("Receipt")+9: selected_receipt.find("Item")-3].strip()
        print (selected_receipt)
        
        self.receipt_shifting(receipt_number)

       
        self.search_window_active = False
        #master.destroy()
    
    def receipt_shifting (self,receipt_number):
        
        receipt_list = MainWindow.receipt_dict[receipt_number]
        MainWindow.index = MainWindow.receipt_list.index(receipt_number)
        
        
            
        self.page_number.config(text= f"{MainWindow.index+1} of {MainWindow.page_amount}")
        print(receipt_list, "receipt list", MainWindow.index, " index")
        print (MainWindow.receipt_dict, "whole dict")

        self.receipt_image.config(text= f"Store \nName: {receipt_list[0]}\n Reciept: {receipt_number}\n Item: {receipt_list[1]}\n Amount:{receipt_list[2]}")
        
        if MainWindow.index+1 == MainWindow.page_amount: 
            self.forward.config(state= DISABLED)
            self.back.config(state= ACTIVE)
        elif MainWindow.index == 0:
            self.forward.config(state= ACTIVE)
            self.back.config(state= DISABLED)
        elif MainWindow.page_amount == 1: 
            self.forward.config(state= DISABLED)
            self.back.config(state= DISABLED)
        else:
            self.forward.config(state= ACTIVE)
            self.back.config(state= ACTIVE)
    def delete (self):
        print(MainWindow.index)
        try:
            receipt_number = MainWindow.receipt_list[MainWindow.index]
            print(receipt_number)
        except IndexError: 
            messagebox.showerror("ERROR", "There are no receipts to return")
        else:
            MainWindow.receipt_dict.pop(receipt_number)
            MainWindow.receipt_list.remove(receipt_number)
            MainWindow.page_amount -= 1 
            MainWindow.index -= 1 
            
            if MainWindow.page_amount == 0: 
                self.receipt_image.config(text= f"No receipts\n\n\n\n")
                self.page_number.config(text = f"{MainWindow.index+1} of {MainWindow.page_amount}")
            else:
                self.receipt_shifting(receipt_number=MainWindow.receipt_list[MainWindow.index])
            
        
    
    def add(self): 
        name = self.name_entry.get().strip()
        item = self.item_entry.get().strip()
        amount = self.amount_entry.get().strip()
        receipt_number = self.receipt_entry.get().strip()
        error = False
        error_text = []
        
        
        
            
            
        if receipt_number in MainWindow.receipt_list or not receipt_number or not receipt_number.isdigit():
            #messagebox.showerror("error", "enter different receipt number")
            
            error = True 
            error_text.append("Receipt-number")
        if any(number.isdigit() for number in name) or not name:
            error = True
            error_text.append("name")
        if  any(number.isdigit() for number in item) or not item:
            error = True 
            error_text.append("item")
        if not amount or not amount.isdigit() or int(amount)>500 or int(amount)<1:
            error = True 
            error_text.append("item-amount")
            
        if error == True: 
            #messagebox.showerror("error", f"Invalid { ' '.join(map(str, error_text))}")
            
            messagebox.showerror("error", f"Invalid { ', '.join(map(str, error_text))}")
        else:
            MainWindow.receipt_dict.update({receipt_number: [name,item, amount]})
            MainWindow.receipt_list.append(receipt_number)
            MainWindow.page_amount += 1
            self.receipt_shifting(receipt_number)
        
        
                      
    
        
        
            
            
    def next_receipt(self): 
        MainWindow.index += 1
        self.forward.config(state=ACTIVE)
        self.back.config(state=ACTIVE)
        
        receipt_number = MainWindow.receipt_list[MainWindow.index]
        self.receipt_shifting(receipt_number)
    def previous_receipt(self): 
        MainWindow.index -= 1
        self.forward.config(state=ACTIVE)
        self.back.config(state= ACTIVE)
        
        
        receipt_number = MainWindow.receipt_list[MainWindow.index]
        print(receipt_number)
        receipt_list = MainWindow.receipt_dict[receipt_number]
        
        self.receipt_shifting(receipt_number)

    def quit (self):
        root.destroy()

    
       

root = Tk()   
program = MainWindow(root)

root.mainloop()
