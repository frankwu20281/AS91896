from tkinter import * 
from tkinter import messagebox
from tkinter import ttk

class MainWindow: 
    
    receipt_list = []
    receipt_dict ={}
    index = -1 
    page_amount = 0 
    def __init__(self, master):
        self.search_window_active = False
        

        self.master = master 
       
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        tool_menu = Menu(menubar, tearoff= 0)
        tool_menu.add_command(label="Advanced Search", command= self.search_window)
        tool_menu.add_command(label= "Exit", command= self.quit)
        menubar.add_cascade(label="Tools", menu= tool_menu )

    
        Label(root,text='Store').pack( anchor=N)

        
        
        
        
        frame = Frame(root)
        frame.pack(expand= True, fill=BOTH)

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
        Button(EntryFrame, text = "Return", command = self.add).grid(row=5,column=1)
       
        


        SearchFrame = LabelFrame(frame, text= "Receipt Search")
        SearchFrame.pack()

        self.search_label = Label(SearchFrame, text= "Search receipts")
        self.search_label.grid(row = 6, column= 0)
        self.search_entry = Entry(SearchFrame)
        self.search_entry.bind("<Return>", (lambda event: self.receipt_search(self)))
        self.search_entry.grid(row = 6, column= 1, columnspan= 3)
        
        
        
        
        DisplayFrame=LabelFrame(frame, text= "Receipt")
        DisplayFrame.pack( fill=  BOTH, expand= TRUE)

        self.receipt_image = Label(DisplayFrame, text="\n\n\n\n")
        self.receipt_image.pack(fill= X)

        self.back = Button(DisplayFrame, text="<-", command= self.previous_receipt, state= DISABLED)
        self.back.pack(side= LEFT)

        self.page_number = Label(DisplayFrame, text= f"{MainWindow.index+1} of {MainWindow.page_amount}")
        self.page_number.pack(side= LEFT,fill= BOTH, expand= True)
        
        self.forward = Button(DisplayFrame, text= "->", command= self.next_receipt, state= DISABLED)
        self.forward.pack(side= LEFT)
        
        #self.search_button = Button(master, text="Search", command= self.search)
        #self.search_button.grid()

    def search_window (self):
        self.search_window_active = True
        self.all = False
        
        
        
        
        
        
        
        self.SearchWindow= Toplevel(root)
        self.SearchWindow.title('NEW')
        Label(self.SearchWindow, text='Advanced Search').pack()
        self.dropdown= StringVar()
        self.dropdown.set("Select Search type")
        
        self.dropdown_menu= OptionMenu(self.SearchWindow, self.dropdown, "Receipt", "Name", "Item", "Search All", command= self.adv_search)
        
        self.dropdown_menu.pack()

        self.adv_search_entry = Entry(self.SearchWindow)
        self.adv_search_entry.bind ("<KeyRelease>", lambda event: self.adv_search(self))
        self.adv_search_entry.pack(padx= 5, fill= X)

        self.receipt_storage = Listbox(self.SearchWindow, width= 50)
        self.receipt_storage.bind('<Double-Button>', (lambda event: self.double_click(self)))
        #self.search_entry.bind("<Return>", (lambda event: self.adv_search(self)))
        self.receipt_storage.pack(pady= 5, padx=5, fill= X, anchor= S)
    


    def adv_search(self, event):
        
        
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
        
            
        
        for a in self.search_list:
            if typed == "":
                self.receipt_storage.insert(END, a)
            elif typed.lower() in a.lower():
                self.receipt_storage.insert(END, a)
                
            
       
            
            
        print ('done')
        

    def name_search(self, event):
        name = self.adv_search_entry.get().strip()
        
        inlist = False

        
        for receipt_number, receipt_list in MainWindow.receipt_dict.items():
            print (list)
            if list[0] == name:
                inlist= True 
                
                MainWindow.index = MainWindow.receipt_list.index(receipt_number)
                self.page_number.config(text = f"{MainWindow.index+1} of {MainWindow.page_amount}")                                
                self.page_number.config(text= f"{MainWindow.index+1} of {MainWindow.page_amount}")
                print(MainWindow.receipt_dict[receipt_number], "yes")
                item_text = f"Name: {receipt_list[0]} - Receipt: {receipt_number} - Item: {receipt_list[1]} - Amount: {receipt_list[2]}"
                self.receipt_storage.insert(END, item_text)
            else:
                print('no')
        
        ###if inlist == False:
            ###messagebox.showerror("error", "receipts with this name not found")###
    
    def item_search(self, event):
        item = self.adv_search_entry.get().strip()
        self.receipt_storage.delete(0, END)
        inlist = False

        
        for receipt_number, receipt_list in MainWindow.receipt_dict.items():
            print (list)
            if list[1] == item:
                inlist= True 
                
                MainWindow.index = MainWindow.receipt_list.index(receipt_number)
                self.page_number.config(text = f"{MainWindow.index+1} of {MainWindow.page_amount}")                                
                self.page_number.config(text= f"{MainWindow.index+1} of {MainWindow.page_amount}")
                print(MainWindow.receipt_dict[receipt_number], "yes")
                item_text = f"Name: {receipt_list[0]} - Receipt: {receipt_number} - Item: {receipt_list[1]} - Amount: {receipt_list[2]}"
                self.receipt_storage.insert(END, item_text)
            else:
                print('no')
        
        #if inlist == False:
            #messagebox.showerror("error", "receipts with this item not found")
        

    def receipt_search (self,event):
        
        if self.search_window_active == True:
            receipt_number = self.adv_search_entry.get()
        else:
            receipt_number = self.search_entry.get()
        if receipt_number in MainWindow.receipt_list: 
            
            receipt_list = MainWindow.receipt_dict[receipt_number]
            MainWindow.index = MainWindow.receipt_list.index(receipt_number)
            self.page_number.config(text = f"{MainWindow.index+1} of {MainWindow.page_amount}")
            
            self.page_number.config(text= f"{MainWindow.index+1} of {MainWindow.page_amount}")
            print(receipt_list, MainWindow.index)

            self.receipt_image.config(text= f"Store  \nName: {receipt_list[0]}\n Reciept: {receipt_number}\n Item: {receipt_list[1]}\n Amount:{receipt_list[2]}")
            if self.search_window_active == True: 

                item_text = f"Name: {receipt_list[0]} - Receipt: {receipt_number} - Item: {receipt_list[1]} Amount: {receipt_list[2]}"
                self.receipt_storage.insert(END, item_text)
        #else: 
            #messagebox.showerror("error", "receipt not found")
            
    def double_click (self, event):
        selected_receipt = self.receipt_storage.get(self.receipt_storage.curselection())
        
        
        print('yes')
        index_start = selected_receipt.find("Re")
        print(index_start)

        index_end = selected_receipt.find("Item")
        print(index_end)
        
        receipt_number = selected_receipt[index_start+9: index_end-3].strip()
        print (selected_receipt)
        
        receipt_list = MainWindow.receipt_dict[receipt_number]
        MainWindow.index = MainWindow.receipt_list.index(receipt_number)
        self.page_number.config(text = f"{MainWindow.index+1} of {MainWindow.page_amount}")
            
        self.page_number.config(text= f"{MainWindow.index+1} of {MainWindow.page_amount}")
        print(receipt_list, MainWindow.index)

        self.receipt_image.config(text= f"Store \nName: {receipt_list[0]}\n Reciept: {receipt_number} Item: {receipt_list[1]}\n Amount:{receipt_list[2]}")
        
        if MainWindow.index+1 == MainWindow.page_amount: 
            self.forward.config(state= DISABLED)
            self.back.config(state= ACTIVE)
        elif MainWindow.index == 0:
            self.forward.config(state= ACTIVE)
            self.back.config(state= DISABLED)
        else:
            self.forward.config(state= ACTIVE)
            self.back.config(state= ACTIVE)

       
        self.search_window_active = False
        #self.SearchWindow.destroy()
        
    def add(self): 
        name = self.name_entry.get().strip()
        item = self.item_entry.get().strip()
        amount = self.amount_entry.get().strip()
        receipt = self.receipt_entry.get().strip()
        
        while True: 
            
            
            if receipt in MainWindow.receipt_list:
                messagebox.showerror("error", "enter different receipt number")
                break
            else:
                MainWindow.receipt_dict.update({receipt: [name,item, amount]})
                MainWindow.receipt_list.append(receipt)
                print (MainWindow.receipt_dict)
                self.receipt_image.config(text= f"Store \nname: {name} \n reciept: {receipt} \n item: {item}\n amount:{amount}")
                
                MainWindow.index = MainWindow.page_amount 
                MainWindow.page_amount += 1
                print(MainWindow.index)
                self.page_number.config(text = f"{MainWindow.index+1} of {MainWindow.page_amount}")
                if MainWindow.page_amount == 1:
                    self.forward.config(state= DISABLED)
                    self.back.config(state= DISABLED)
                else:
                    self.forward.config(state= DISABLED)
                    self.back.config(state= ACTIVE)
                break 

    def next_receipt(self): 
        MainWindow.index += 1
        self.forward.config(state=ACTIVE)
        self.back.config(state=ACTIVE)
        
        receipt_number = MainWindow.receipt_list[MainWindow.index]
        print(receipt_number)
        receipt_list = MainWindow.receipt_dict[receipt_number]
        
        
        self.page_number.config(text= f"{MainWindow.index+1} of {MainWindow.page_amount}")
        print(receipt_list, MainWindow.index)

        self.receipt_image.config(text= f"Store \nname: {receipt_list[0]} \n reciept: {receipt_number} \n item: {receipt_list[1]}\n amount:{receipt_list[2]}")
        
        if MainWindow.index+1 == MainWindow.page_amount:
            self.forward.config(state=DISABLED)
        else:
            self.forward.config(state= ACTIVE)
        
    
    def previous_receipt(self): 
        MainWindow.index -= 1
        self.forward.config(state=ACTIVE)
        self.back.config(state= ACTIVE)
        
        
        receipt_number = MainWindow.receipt_list[MainWindow.index]
        print(receipt_number)
        receipt_list = MainWindow.receipt_dict[receipt_number]
        
        self.page_number.config(text= f"{MainWindow.index+1} of {MainWindow.page_amount}")
        print(receipt_list, MainWindow.index)

        self.receipt_image.config(text= f"Store \nname: {receipt_list[0]} \n reciept: {receipt_number} \n item: {receipt_list[1]}\n amount:{receipt_list[2]}")

        if MainWindow.index == 0:
            self.back.config(state=DISABLED)
        else:
            self.back.config(state= ACTIVE)

    def quit (self):
        root.destroy()

    
       

root = Tk()   
program = MainWindow(root)

root.mainloop()
