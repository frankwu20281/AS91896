from tkinter import * 
from tkinter import messagebox





class MainWindow: 
    
    receipt_list = []
    receipt_dict ={}
    index = -1 
    page_amount = 0 
    def __init__(self, master):
        

        self.master = master 
       
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        tool_menu = Menu(menubar, tearoff= 0)
        tool_menu.add_command(label="Advanced Search", command= self.search_window)
        tool_menu.add_command(label= "Exit", command= self.quit)
        menubar.add_cascade(label="Tools", menu= tool_menu )

    



        Label(master,text= 'Store').grid(row=0, column=0, columnspan= 2)
         
        self.name_label = Label(master, text= "enter full name")
        self.name_label.grid(row=1, column=0)
        self.name_entry = Entry(master)
        self.name_entry.grid(row=1, column=1)


        self.receipt_label = Label(master, text = "enter receipt number")
        self.receipt_label.grid(row= 2, column= 0)
        self.receipt_entry = Entry(master)
        self.receipt_entry.grid(row=2, column=1 )

        self.item_label = Label(master, text= "enter item name")
        self.item_label.grid(row=3, column= 0)
        self.item_entry = Entry(master)
        self.item_entry.grid(row=3, column=1)

        self.amount_label = Label(master, text= "enter item amount")
        self.amount_label.grid(row=4, column= 0)
        self.amount_entry = Entry(master)
        self.amount_entry. grid (row=4, column=1)


        #self.receipt_storage = Listbox(master)
        #self.receipt_storage.grid(columnspan= 2)

        Button(master, text= "Buy", command= self.add).grid(row=5, column=0)
        Button(master, text = "Return", command = self.add).grid(row=5,column=1)
        
        self.receipt_image = Label(master, text="")
        self.receipt_image.grid(row= 6, column=0, columnspan= 2)

        self.forward = Button(master, text= "->", command= self.next_receipt, state= DISABLED)
        self.forward.grid(row=7, column=1)
        

        self.back = Button(master, text="<-", command= self.previous_receipt, state= DISABLED)
        self.back.grid(row= 7, column=0 )

        self.page_number = Label(master, text= f"{MainWindow.index+1} of {MainWindow.page_amount}")
        self.page_number.grid(row = 8, column= 0, columnspan= 2)

       
      
        self.search_label = Label(master, text= "Search receipts")
        self.search_label.grid(row = 9, column= 0)
        self.search_entry = Entry(master)
        self.search_entry.bind("<Return>", (lambda event: self.search(self)))
        self.search_entry.grid(row = 9, column= 1)

        
        #self.search_button = Button(master, text="Search", command= self.search)
        #self.search_button.grid()

    def search_window (self):
        
        SearchWindow= Toplevel(root)
        SearchWindow.title('NEW')
        Label(SearchWindow, text='Advanced Search').grid(row=0, column=0, columnspan=2 )
        self.dropdown= StringVar()
        self.dropdown.set("Select Search type")
        
        self.dropdown_menu= OptionMenu(SearchWindow, self.dropdown, "Receipt", "Name", "Item", "Amount")
        self.dropdown_menu.grid(row=1,column=0)

        self.search_entry = Entry(SearchWindow)
        self.search_entry.bind("<Return>", (lambda event: self.adv_search(self)))
        self.search_entry.grid(row=1, column= 1)

        self.receipt_storage = Listbox(SearchWindow)
        self.receipt_storage.grid(columnspan= 2)

    def adv_search(self, event):
        choice = self.dropdown.get()
        if choice == "Name":
            MainWindow.search_name(self, event)
        elif choice =="Receipt":
            MainWindow.search(self, event) 

    def search_name(self, event):
        name = self.search_entry.get()
        self.receipt_storage.delete(0, END)
        inlist = False

        
        for receipt_number, list in MainWindow.receipt_dict.items():
            print (list)
            if list[0] == name:
                inlist= True 
                receipt_list = MainWindow.receipt_dict[receipt_number]
                MainWindow.index = MainWindow.receipt_list.index(receipt_number)
                self.page_number.config(text = f"{MainWindow.index+1} of {MainWindow.page_amount}")                                
                self.page_number.config(text= f"{MainWindow.index+1} of {MainWindow.page_amount}")
                print(MainWindow.receipt_dict[receipt_number], "yes")
                item_text = f"{receipt_list[0]} - {receipt_number} - {receipt_list[1]}({receipt_list[2]})"
                self.receipt_storage.insert(END, item_text)
            else:
                print('no')
        
        if inlist == False:
            messagebox.showerror("error", "receipt not found")
        

    def search (self,event):
        receipt_number = self.search_entry.get()

        if receipt_number in MainWindow.receipt_list: 
            
            receipt_list = MainWindow.receipt_dict[receipt_number]
            MainWindow.index = MainWindow.receipt_list.index(receipt_number)
            self.page_number.config(text = f"{MainWindow.index+1} of {MainWindow.page_amount}")
            
            self.page_number.config(text= f"{MainWindow.index+1} of {MainWindow.page_amount}")
            print(receipt_list, MainWindow.index)

            self.receipt_image.config(text= f"Store\n reciept: {receipt_number} \nname: {receipt_list[0]}\n item: {receipt_list[1]}\n amount:{receipt_list[2]}")
        else: 
            messagebox.showerror("error", "receipt not found")
        
    def add(self): 
        name = self.name_entry.get()
        item = self.item_entry.get()
        amount = self.amount_entry.get()
        receipt = self.receipt_entry.get()
        
        while True: 
            
            
            if receipt in MainWindow.receipt_list:
                messagebox.showerror("error", "enter different receipt number")
                break
            else:
                MainWindow.receipt_dict.update({receipt: [name,item, amount]})
                MainWindow.receipt_list.append(receipt)
                print (MainWindow.receipt_dict)
                self.receipt_image.config(text= f"Store\n reciept: {receipt} \nname: {name}\n item: {item}\n amount:{amount}")
                
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

        #item_text = f"{name} - {receipt_number} - {item}({amount})"
        #self.receipt_storage.insert(END, item_text)

    def next_receipt(self): 
        MainWindow.index += 1
        self.forward.config(state=ACTIVE)
        self.back.config(state=ACTIVE)
        
        receipt_number = MainWindow.receipt_list[MainWindow.index]
        print(receipt_number)
        receipt_list = MainWindow.receipt_dict[receipt_number]
        
        
        self.page_number.config(text= f"{MainWindow.index+1} of {MainWindow.page_amount}")
        print(receipt_list, MainWindow.index)

        self.receipt_image.config(text= f"Store\n reciept: {receipt_number} \nname: {receipt_list[0]}\n item: {receipt_list[1]}\n amount:{receipt_list[2]}")
        
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

        self.receipt_image.config(text= f"Store\n reciept: {receipt_number} \nname: {receipt_list[0]}\n item: {receipt_list[1]}\n amount:{receipt_list[2]}")

        if MainWindow.index == 0:
            self.back.config(state=DISABLED)
        else:
            self.back.config(state= ACTIVE)

    def quit (self):
        root.destroy()

    
       

root = Tk()   
program = MainWindow(root)

root.mainloop()
