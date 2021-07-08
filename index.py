from tkinter import ttk
from tkinter import *

import sqlite3

class Product():

    db_name = 'database.db'
    #port = 3307

    def __init__(self, window):

        self.w = window
        self.w.title('Products Application')

        # Creating a Frame Container
        frame = LabelFrame(self.w, text ='Registra un nuevo Producto')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Name input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row =1, column = 1)

        # Price input
        Label(frame, text = 'Price: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        # Button Add Product
        ttk.Button(frame, text = 'Save Product', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

        # Output messages
        
        self.message = Label(text = '', fg = 'dodger blue')
        self.message.grid(row = 3, column = 0, columnspan = 2,sticky = W +E )
        

        # Create table
        self.tree = ttk.Treeview(height = 10, column = 2)
        self.tree.grid(row = 4, column =0, columnspan = 2)
        self.tree.heading('#0', text = 'Name', anchor = CENTER)
        self.tree.heading('#1', text = 'Price', anchor = CENTER)


        ## Buttons
        ttk.Button(text = 'DELETE', command = self.delete_product).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'EDIT', command = self.edit_product).grid(row = 5, column = 1, sticky = W + E)

        # Filling the Row

        self.get_products()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
            return result

    def get_products(self):
        # Cleaning table

        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

         # quering data   
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            #print(row)
            self.tree.insert('', 0, text = row[1], values = row [2])

    
    def validation(self):
        # Si name y price no estan vacios genera un True
        return len(self.name.get()) != 0 and len(self.price.get()) != 0



    def add_product(self):
        # Si valitation es True... haz:
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters = (self.name.get(),self.price.get())
            self.run_query(query, parameters)
            
            self.message['text'] = 'Product {} was added Successfully'.format(self.name.get())
            # Limpiar todo de nuevo:
            self.name.delete(0, END)
            self.price.delete(0, END)
            #print('Data saved')
            #print(self.name.get())
            #print(self.price.get())
        else:

            
            self.message['text'] = 'Name and Price are Required'
        self.get_products()


    def delete_product(self):

        self.message['text'] = ''
        self.message['fg'] = '#800000'
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please Select a Record'
            return
        self.message['text'] = ''    
        name = self. tree.item(self.tree.selection())['text']    
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name,))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_products()


    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please Select a Record'
            return
        #self.message['text'] = ''  
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_window = Toplevel()
        self.edit_window.title = 'Edit Product'


        # Old Name
        Label(self.edit_window, text = 'Old Name: ').grid(row = 0, column = 1)
        Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = name), state = 'readonly').grid(row = 0, column = 2)

        # New name
        Label(self.edit_window, text = 'New Name: ').grid(row = 1, column = 1)
        new_name = Entry(self.edit_window)
        new_name.grid(row = 1, column = 2)


        
        # Old Price
        Label(self.edit_window, text = 'Old Price: ').grid(row = 2, column = 1)
        Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = old_price), state = 'readonly').grid(row = 2, column = 2)

        # New Price
        Label(self.edit_window, text = 'New Price: ').grid(row = 3, column = 1)
        new_price = Entry(self.edit_window)
        new_price.grid(row = 3, column = 2)
        # Buttton update
        #Button(self.edit_window, text = 'Update', command = lambda: self.edit_records(new_name.get(), name, new_price.get(),old_price)).grid(row = 4, column = 2, sticky = W + E)
        Button(self.edit_window, text = 'Update', command = lambda: self.edit_records(new_name.get(), name, new_price.get(),old_price)).grid(row = 4, column = 2, sticky = W + E)


    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_window.destroy()
        self.message['text'] = 'Record {} updated Successfully'.format(name)
        self.get_products()


if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
