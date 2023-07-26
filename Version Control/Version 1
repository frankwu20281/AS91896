from tkinter import * 
from tkinter import messagebox

import random


class MainWindow: 
    receipt_list = []
    receipt_dict ={}
    page= -1 
    page_amount = 0 
    def __init__(self, master):
        self.master = master 
        
        


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

        
        self.receipt_image = Label(master, text="")
        self.receipt_image.grid(row= 6, column=0, columnspan= 2)

        self.forward = Button(master, text= "->", command= self.next_receipt)

        self.forward.grid(row=7, column=1)

        self.back = Button(master, text="<-", command= self.previous_receipt)
        self.back.grid(row= 7, column=0 )

        self.page_number = Label(master, text= f"{MainWindow.page+1} of {MainWindow.page_amount}")
        self.page_number.grid()

        Button(master, text= "Buy", command= self.add).grid(row=5, column=0)
        Button(master, text = "Return", command = self.add).grid(row=5,column=1)
        Button(master, text = "quit", command = self.quit).grid(row=8,column=1)


        
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
                
                MainWindow.page += 1 
                MainWindow.page_amount += 1
                print(MainWindow.page)
                self.page_number.config(text = f"{MainWindow.page+1} of {MainWindow.page_amount}")
                break 

        #item_text = f"{name} - {receipt_number} - {item}({amount})"
        #self.receipt_storage.insert(END, item_text)

    def next_receipt(self): 
        MainWindow.page += 1
        
        receipt_number = MainWindow.receipt_list[MainWindow.page]
        print(receipt_number)
        receipt_list = MainWindow.receipt_dict[receipt_number]
        
        
        self.page_number.config(text= f"{MainWindow.page+1} of {MainWindow.page_amount}")
        print(receipt_list, MainWindow.page)

        self.receipt_image.config(text= f"Store\n reciept: {receipt_number} \nname: {receipt_list[0]}\n item: {receipt_list[1]}\n amount:{receipt_list[2]}")
        
    
    def previous_receipt(self): 
        MainWindow.page -= 1
        
        
        receipt_number = MainWindow.receipt_list[MainWindow.page]
        print(receipt_number)
        receipt_list = MainWindow.receipt_dict[receipt_number]
        
        self.page_number.config(text= f"{MainWindow.page+1} of {MainWindow.page_amount}")
        print(receipt_list, MainWindow.page)

        self.receipt_image.config(text= f"Store\n reciept: {receipt_number} \nname: {receipt_list[0]}\n item: {receipt_list[1]}\n amount:{receipt_list[2]}")

    

    def quit (self):
        root.destroy()

    
       

root = Tk()   
program = MainWindow(root)
root.mainloop()
