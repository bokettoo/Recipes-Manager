import tkinter as tk
from tkinter import ttk
from tkinter import messagebox 
import pymysql
import random
from ttkthemes import ThemedStyle
import datetime
passwd = ""

class RecipesManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipes Manager")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#2b2b2b")  # Dark background color

        self.style = ThemedStyle(self.root)
        self.style.set_theme("equilux")  # Set theme to Equilux

        self.notebook = ttk.Notebook(self.root, width=1400, height=900)
        
        style = ttk.Style()
        style.configure("TNotebook.Tab", padding=[97, 5], font=("Helvetica", 12, "bold"), foreground="white")

        self.notebook.pack(padx=20, pady=20)

        self.home_page = ttk.Frame(self.notebook)
        self.notebook.add(self.home_page, text="Home")

        self.add_recipe_page = ttk.Frame(self.notebook)
        self.notebook.add(self.add_recipe_page, text="Add Recipe")

        self.shuffle_recipes_page = ttk.Frame(self.notebook)
        self.notebook.add(self.shuffle_recipes_page, text="Shuffle Recipes")

        self.search_recipe_page= ttk.Frame(self.notebook)
        self.notebook.add(self.search_recipe_page, text="Search")

        self.manage_recipes_page = ttk.Frame(self.notebook)
        self.notebook.add(self.manage_recipes_page, text="Manage Recipes")

        self.create_home_page()
        self.create_add_recipe_page()
        self.create_shuffle_recipes_page()
        self.create_manage_recipes_page()
        self.create_search_page()

        self.notebook.select(self.home_page)
    
    @staticmethod
    def update_time():
        while True:
            clock = datetime.datetime.now().strftime("%H:%M:%S")
            return str(clock)
    @staticmethod
    def update_label(label):
        current_time = RecipesManager.update_time()
        label.config(text=current_time)
        label.after(1000, RecipesManager.update_label, label)

    @staticmethod
    def update_welcoming(label):
        current_time = datetime.datetime.now()
        hour = current_time.hour
        if 6 <= hour < 12:
            greeting = "Good morning!"
        elif 12 <= hour < 18:
            greeting = "Good afternoon!"
        elif 18 <= hour < 22:
            greeting = "Good evening!"
        else:
            greeting = "Good night!"
        label.config(text=greeting)   
    
    @staticmethod
    def recipe_count():
        conn = pymysql.connect(host='127.0.0.1', user='root', password=passwd, db='recipe_db')
        c= conn.cursor()

        query= "SELECT * FROM recipes"

        c.execute(query)

        rows = c.fetchall()

        return str(len(rows))
    
    @staticmethod
    def update_recipe_count(label):
        count = RecipesManager.recipe_count()
        label.config(text= f"{count} recipes saved.")
        label.after(1000, RecipesManager.update_recipe_count, label)
    @staticmethod
    def copy_to_clipboard(tree):
        selected_item = tree.focus()  
        if selected_item:
            item_text = tree.item(selected_item)['values']  
            root.clipboard_clear()  
            root.clipboard_append(item_text)  
            messagebox.showinfo("Done.","Recipe copied to clipboard")
        else: 
            messagebox.showwarning("","Please select a row to copy")
    
    def copy_to_clipboard_suffle(self):
        self.copy_to_clipboard(self.tree_view1)
    
    def copy_to_clipboard_search(self):
        self.copy_to_clipboard(self.tree_view2)
    
    def copy_to_clipboard_manage(self):
        self.copy_to_clipboard(self.tree_view)

    def create_edit_menu(self):
        self.popup = tk.Toplevel(root)
        self.popup.title("Popup Window")
        self.popup.geometry("500x500")
        self.popup.configure(bg="#2b2b2b")  # Dark background color

        window_bg_color = self.popup.cget("bg")


        name_label = ttk.Label(self.popup, text="Name:",foreground="white",font=('Helvetica', 12),background=window_bg_color)
        name_label.pack(pady=10)

        self.name_entry_pop = ttk.Entry(self.popup,foreground="white",font=('Helvetica', 12))
        self.name_entry_pop.pack(pady=10)
        
        ingredients_label = ttk.Label(self.popup, text="Ingredients:",foreground="white",font=('Helvetica', 12),background=window_bg_color)
        ingredients_label.pack(pady=20)

        self.ingredients_entry_pop = tk.Text(self.popup, height=10, bg=self.style.lookup("TEntry", "background"),font=("Helvetica", 12),foreground="white")
        self.ingredients_entry_pop.pack(pady=10)
        
        instructions_label = ttk.Label(self.popup, text="Instructions:",foreground="white",font=('Helvetica', 12),background=window_bg_color)
        instructions_label.pack()

        self.instructions_entry_pop = tk.Text(self.popup, height=10, bg=self.style.lookup("TEntry", "background"),font=("Helvetica", 12),foreground="white")
        self.instructions_entry_pop.pack(pady=10)
        
        edit_button = ttk.Button(self.popup, text="Edit Recipe", command=self.edit_recipe)
        edit_button.pack(pady=20)

        self.style = ttk.Style()
        self.style.configure("Custom.TButton", foreground="white", background="#3c3f41", relief="raised", font=('Helvetica', 12))

        edit_button.config(style="Custom.TButton")

        self.load_edit_recipe()
    
    
    def create_home_page(self):

        time_label = ttk.Label(self.home_page, font=("Helvetica", 9), foreground="white")
        time_label.pack(side=tk.RIGHT, anchor=tk.NE, padx=10)  
        self.update_label(time_label)
        
        welcoming = ttk.Label(self.home_page, font=("Helvetica", 9), foreground="white")
        welcoming.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)  
        self.update_welcoming(welcoming)

        welcome_label = ttk.Label(self.home_page, text="Welcome to Recipes Manager!", font=("Helvetica", 24))
        welcome_label.pack(pady=20)
        
        intro_label_text = """This handy tool helps you organize and manage all your favorite recipes in one place. Whether you're a cooking enthusiast or just looking to streamline your meal planning, Recipes Manager makes it easy to add, search, shuffle, and manage your recipes effortlessly. Get ready to explore a world of culinary delights with just a few clicks!"""

        intro_label = ttk.Label(self.home_page, text=intro_label_text, wraplength=500,anchor="center",justify="center",font=("Helvetica",14))
        intro_label.pack(pady=20, padx=20)

        home_nav = ttk.Frame(self.home_page)
        home_nav.pack()

        add_recipe_button = ttk.Button(home_nav, text="Add Recipe", command=lambda: self.notebook.select(self.add_recipe_page))
        add_recipe_button.pack()

        self.style = ttk.Style()
        self.style.configure("Custom.TButton", foreground="white", background="#3c3f41", relief="raised", font=('Helvetica', 12))
        
        add_recipe_button.config(style="Custom.TButton")
   

    def create_add_recipe_page(self):
        time_label = ttk.Label(self.add_recipe_page, font=("Helvetica", 9), foreground="white")
        time_label.pack(side=tk.RIGHT, anchor=tk.NE, padx=10)  # Pack time_label to the top right corner
        self.update_label(time_label)

        name_label = ttk.Label(self.add_recipe_page, text="Name:",foreground="white",font=('Helvetica', 12))
        name_label.pack()

        self.name_entry = ttk.Entry(self.add_recipe_page,foreground="white",font=('Helvetica', 12))
        self.name_entry.pack(pady=10)
        

        recipe_type= ttk.Label(self.add_recipe_page, text="Type",foreground="white",font=('Helvetica', 12))
        recipe_type.pack()

        options = ["Breakfast","Lunch","Dinner"]
        selected_option = tk.StringVar(self.add_recipe_page)
        selected_option.set(options[0])

 
        self.select_menu = ttk.Combobox(self.add_recipe_page, textvariable=selected_option, values=options)
        self.select_menu.pack(pady=10)
        
        ingredients_label = ttk.Label(self.add_recipe_page, text="Ingredients:",foreground="white",font=('Helvetica', 12))
        ingredients_label.pack(pady=20)

        self.ingredients_entry = tk.Text(self.add_recipe_page, height=10, bg=self.style.lookup("TEntry", "background"),font=("Helvetica", 12),foreground="white")
        self.ingredients_entry.pack(pady=10)
        
        instructions_label = ttk.Label(self.add_recipe_page, text="Instructions:",foreground="white",font=('Helvetica', 12))
        instructions_label.pack()

        self.instructions_entry = tk.Text(self.add_recipe_page, height=10, bg=self.style.lookup("TEntry", "background"),font=("Helvetica", 12),foreground="white")
        self.instructions_entry.pack(pady=10)
        
        add_button = ttk.Button(self.add_recipe_page, text="Add Recipe", command=self.add_recipe)
        add_button.pack(pady=20)

        self.style = ttk.Style()
        self.style.configure("Custom.TButton", foreground="white", background="#3c3f41", relief="raised", font=('Helvetica', 12))

        add_button.config(style="Custom.TButton")

    def add_recipe(self):
        name = self.name_entry.get()
        ingredients = self.ingredients_entry.get("1.0", tk.END)
        instructions = self.instructions_entry.get("1.0", tk.END)
        selected_value = self.select_menu.get()

        if not name or not ingredients or not instructions or not selected_value:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            conn = pymysql.connect(host='127.0.0.1', user='root', password=passwd, db='recipe_db')
            c = conn.cursor()
            query_1 = "INSERT INTO recipes (name, ingredients, instructions) VALUES (%s, %s, %s)"
            query_2 = "INSERT INTO recipe_types (id,type) VALUES (%s, %s)"
            c.execute(query_1, (name, ingredients, instructions))
            conn.commit()
            recipe_id = c.lastrowid
            c.execute(query_2, (recipe_id,selected_value))
            conn.commit()
            messagebox.showinfo("Success", "Recipe added successfully.")
        except pymysql.Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def create_shuffle_recipes_page(self):
        time_label = ttk.Label(self.shuffle_recipes_page, font=("Helvetica", 9), foreground="white")
        time_label.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)  # Pack time_label to the top right corner
        self.update_label(time_label)

        options = ["breakfast","lunch","dinner"]
        selected_option = tk.StringVar(self.shuffle_recipes_page)
        selected_option.set(options[0])

        recipe_type= ttk.Label(self.shuffle_recipes_page, text="Type",foreground="white",font=('Helvetica', 12))
        recipe_type.pack()
        self.select_menu1 = ttk.Combobox(self.shuffle_recipes_page, textvariable=selected_option, values=options)
        self.select_menu1.pack(pady=10)
        

        shuffle_button = ttk.Button(self.shuffle_recipes_page, text="Shuffle", command=self.shuffle_recipes)
        shuffle_button.pack(pady=10)
        
        copy_button = ttk.Button(self.shuffle_recipes_page, text="Copy", command=self.copy_to_clipboard_suffle)
        copy_button.pack(pady=10)

        self.style = ttk.Style()
        self.style.configure("Custom.TButton", foreground="white", background="#3c3f41", relief="raised", font=('Helvetica', 12))

        shuffle_button.config(style="Custom.TButton")
        copy_button.config(style="Custom.TButton")

        self.tree_view1 = ttk.Treeview(self.shuffle_recipes_page,show="headings", columns=("ID", "name", "ingredients", "instructions"))
        self.tree_view1.pack(fill=tk.BOTH,expand=True,padx=50, pady=50)
        self.tree_view1.heading("ID", text="ID")
        self.tree_view1.heading("name", text="Name")
        self.tree_view1.heading("ingredients", text="Ingredients")
        self.tree_view1.heading("instructions", text="Instructions")
        self.tree_view1.column("ID", width=1)
        self.tree_view1.column("name", width=200)
        self.tree_view1.column("ingredients", width=300)
        self.tree_view1.column("instructions", width=400)

    def shuffle_recipes(self):
        selected_value = self.select_menu1.get()
        if not selected_value:
            messagebox.showerror("Error", "All fields are required.")
            return
        else:

            try:
                conn = pymysql.connect(host='127.0.0.1', user='root', password=passwd, db='recipe_db')
                
                c=conn.cursor() 
                
                query = "SELECT * FROM recipe_types WHERE `type`=%s"
                
                c.execute(query,selected_value)
                
                rows = c.fetchall()

                if len(rows) == 0:
                    messagebox.showerror("Error", "No recipes found.")
                    return

                random_index = random.randint(0, len(rows) - 1)
                random_type = rows[random_index]
                

                query = "SELECT * FROM recipes WHERE `id`=%s"
                c.execute(query,random_type[0])
                sub_rows = c.fetchall()

                self.tree_view1.delete(*self.tree_view1.get_children())

                self.tree_view1.insert("", 'end', values=(sub_rows[0]))

                messagebox.showinfo("Random Recipe", "The recipe of the day!")
            except pymysql.Error as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    def create_search_page(self):
        time_label = ttk.Label(self.search_recipe_page, font=("Helvetica", 9), foreground="white")
        time_label.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)  # Pack time_label to the top right corner
        self.update_label(time_label)
        
        search_entry=ttk.Entry(self.search_recipe_page)
        search_entry.pack(pady=10)
        
        submit_button=ttk.Button(self.search_recipe_page, text="Submit", command=lambda: self.search_results(search_entry.get()))
        submit_button.pack()

        copy_button = ttk.Button(self.search_recipe_page, text="Copy", command=self.copy_to_clipboard_search)
        copy_button.pack(padx=10, pady=10)

        self.style = ttk.Style()
        self.style.configure("Custom.TButton", foreground="white", background="#3c3f41", relief="raised", font=('Helvetica', 12))

        submit_button.config(style="Custom.TButton")
        copy_button.config(style="Custom.TButton")

        self.tree_view2 = ttk.Treeview(self.search_recipe_page,show="headings", columns=("ID", "name", "ingredients", "instructions"))
        self.tree_view2.pack(fill=tk.BOTH,expand=True,padx=50, pady=50)
        self.tree_view2.heading("ID", text="ID")
        self.tree_view2.heading("name", text="Name")
        self.tree_view2.heading("ingredients", text="Ingredients")
        self.tree_view2.heading("instructions", text="Instructions")
        self.tree_view2.column("ID", width=5)
        self.tree_view2.column("name", width=200)
        self.tree_view2.column("ingredients", width=300)
        self.tree_view2.column("instructions", width=400)

    def search_results(self,recipe_name):
        try:
            conn = pymysql.connect(host='127.0.0.1', user='root', password=passwd, db='recipe_db')

            c = conn.cursor()

            c.execute("select * from recipes WHERE name=%s", (recipe_name,))
            results = c.fetchall()

            self.tree_view2.delete(*self.tree_view2.get_children())

            if len(results) == 0:
                messagebox.showerror("Error","No recipes found")
                return

            for recipe in results:
                self.tree_view2.insert("", 'end', values=(recipe[0], recipe[1], recipe[2], recipe[3]))
            conn.close()

            messagebox.showinfo("Info", "Recipe found.")
        except pymysql.Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()


    def create_manage_recipes_page(self):
        top_frame = ttk.Frame(self.manage_recipes_page)
        top_frame.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        time_label = ttk.Label(self.manage_recipes_page, font=("Helvetica", 9), foreground="white")
        time_label.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)  # Pack time_label to the top right corner
        self.update_label(time_label)

        recipe_type = ttk.Label(top_frame, text="Type", foreground="white", font=('Helvetica', 12))
        recipe_type.pack(side=tk.LEFT, padx=5, pady=5)

        options = ["All","breakfast","lunch","dinner"]
        selected_option = tk.StringVar()
        self.select_menu2 = ttk.Combobox(top_frame, textvariable=selected_option, values=options)
        self.select_menu2.pack(side=tk.LEFT, padx=5, pady=5)

        load_button = ttk.Button(top_frame, text="Load", command=self.load_recipes)
        load_button.pack(side=tk.LEFT, padx=5, pady=5)

        popup_button = ttk.Button(top_frame, text="Edit", command=self.create_edit_menu)
        popup_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = ttk.Button(top_frame, text="Delete", command=self.delete_recipe)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        copy_button = ttk.Button(top_frame, text="Copy", command=self.copy_to_clipboard_manage)
        copy_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.style = ttk.Style()
        self.style.configure("Custom.TButton", foreground="white", background="#3c3f41", relief="raised", font=('Helvetica', 12))

        delete_button.config(style="Custom.TButton")
        load_button.config(style="Custom.TButton")
        copy_button.config(style="Custom.TButton")
        popup_button.config(style="Custom.TButton")

        bottom_frame = ttk.Frame(self.manage_recipes_page)
        bottom_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        recipe_count = ttk.Label(bottom_frame, text=self.recipe_count(), font=("Helvetica", 10), foreground="white")
        recipe_count.pack(pady=5)
        self.update_recipe_count(recipe_count)


        self.tree_view = ttk.Treeview(bottom_frame, show="headings", columns=("ID", "name", "ingredients", "instructions"))
        self.tree_view.pack(fill=tk.BOTH, expand=True)
        self.tree_view.heading("ID", text="ID")
        self.tree_view.heading("name", text="Name")
        self.tree_view.heading("ingredients", text="Ingredients")
        self.tree_view.heading("instructions", text="Instructions")
        self.tree_view.column("ID", width=1)
        self.tree_view.column("name", width=200)
        self.tree_view.column("ingredients", width=300)
        self.tree_view.column("instructions", width=400)
            

    def load_recipes(self):
        selected_value = self.select_menu2.get()
        if not selected_value:
            messagebox.showinfo("Info","Please select a type of recipe")
        else:
            if selected_value == "All":

                try:
                    conn = pymysql.connect(host='127.0.0.1', user='root', password=passwd, db='recipe_db')

                    c = conn.cursor()

                    c.execute("SELECT * FROM recipes")

                    self.tree_view.delete(*self.tree_view.get_children())

                    for recipe in c.fetchall():
                        self.tree_view.insert("", 'end', values=(recipe[0], recipe[1], recipe[2], recipe[3]))

                    conn.close()

                    messagebox.showinfo("Info", "Recipes loaded successfully.")
                except pymysql.Error as e:
                    messagebox.showerror("Error", str(e))
            else:
                try:
                    conn = pymysql.connect(host='127.0.0.1', user='root', password=passwd, db='recipe_db')
                    
                    c=conn.cursor() 
                    
                    query = "SELECT * FROM recipe_types WHERE `type`=%s"
                    
                    c.execute(query,selected_value)
                    
                    rows = c.fetchall()

                    self.tree_view.delete(*self.tree_view.get_children())

                    for i in range(len(rows)):
                        row = rows[i]
                        query = "SELECT * FROM recipes WHERE `id`=%s"
                        c.execute(query,row[0])
                        result = c.fetchall()
                        self.tree_view.insert("", 'end', values=(result[0]))
                    messagebox.showinfo("Info","Recipe loaded")

                except pymysql.Error as e:
                    messagebox.showerror("Error", f"Error {e}")
    def load_edit_recipe(self):
        selected_recipe = self.tree_view.focus()
        if selected_recipe:
            recipe=self.tree_view.item(selected_recipe)['values']
            self.name_entry_pop.insert(tk.END, recipe[1])
            self.ingredients_entry_pop.insert(tk.END, recipe[2])
            self.instructions_entry_pop.insert(tk.END, recipe[3])
        else:
            messagebox.showerror("Error","Select a recipe")
    
    def edit_recipe(self):
        selected_recipe = self.tree_view.focus()
        recipe=self.tree_view.item(selected_recipe)['values']
        try:
            conn = pymysql.connect(host='127.0.0.1', user='root', password=passwd, db='recipe_db')
            c = conn.cursor()
            query = "UPDATE recipes SET `name` = %s, `ingredients` = %s, `instructions` = %s WHERE id = %s;"
            c.execute(query,(self.name_entry_pop.get(),self.ingredients_entry_pop.get("1.0", tk.END),self.instructions_entry_pop.get("1.0", tk.END),recipe[0]))
            conn.commit()
            messagebox.showinfo("Success", "Recipe updated successfully.")
        except pymysql.Error as e:
            messagebox.showerror("Error", f"{e}")

    def delete_recipe(self):
        selected_recipe = self.tree_view.focus()

        if selected_recipe:
            recipe_name = self.tree_view.item(selected_recipe)['values'][1]

            try:
                conn = pymysql.connect(host='127.0.0.1', user='root', password=passwd, db='recipe_db')

                c = conn.cursor()

                c.execute("DELETE FROM recipes WHERE name=%s", (recipe_name,))

                conn.commit()

                messagebox.showinfo("Success", "Recipe deleted successfully!")

                conn.close()

            except pymysql.Error as e:
                messagebox.showerror("Error", f"Error {e.args[0]}: {e.args[1]}")
        else:
            messagebox.showerror("Error", "No recipe is selected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RecipesManager(root)
    root.mainloop()
