import customtkinter as CTk
from tkinter import messagebox
import tkinter as Tk
import json
import re

# Display of marks in the table

class StudentRecordApp:
    def __init__(self, root, app):
        self.app = app
        self.root = root
        self.root.title("Student Records")
        screen_width = self.root.winfo_screenwidth()
        window_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{window_height}")
        self.root.resizable(True, True)

        # Frame for the search bar and add button
        search_frame = Tk.Frame(self.root)
        search_frame.pack(side=Tk.TOP, fill=Tk.X, pady=5)

        # Search bar
        self.search_var = Tk.StringVar()
        self.search_entry = Tk.Entry(search_frame, textvariable=self.search_var, font=("Helvetica", 20))
        self.search_entry.insert(0, "Rechercher un étudiant")
        self.search_entry.bind("<FocusIn>", self.on_entry_click)
        self.search_entry.bind("<FocusOut>", self.on_focus_out)
        self.search_entry.pack(side=Tk.LEFT, padx=(300, 5), fill=Tk.X, expand=True)

        self.search_button = Tk.Button(search_frame, text="🔍 Rechercher", command=self.search_student, font=("Helvetica", 20), bg="#2196F3")
        self.search_button.pack(side=Tk.LEFT, padx=5)

        # Add button frame
        add_button_frame = Tk.Frame(self.root, bg="#f0f0f0")
        add_button_frame.pack(side=Tk.TOP, fill=Tk.X, padx=10, pady=5)

        # Add button
        self.add_button = Tk.Button(add_button_frame, text="➕ Add a new student", font=("Helvetica", 20), bg="#4CAF50", fg="#ffffff", relief="raised", bd=2, command=self.app.student_record_page)
        self.add_button.pack(side=Tk.LEFT, padx=(700, 5), pady=15)

        # Create a canvas and a scrollbar
        self.canvas = Tk.Canvas(self.root)
        self.canvas.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=True)

        self.scrollbar = Tk.Scrollbar(self.root, orient=Tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create a frame inside the canvas
        self.table_frame = Tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        # Add headers
        self.headers = ["ID", "Name", "Class", "Analysis", "Algebra", "Algorithm", "English", "Mathematics", "Physics", "Chemistry", "Biology", "Arts", "Informatique", "Average","Actions"]
        for col, header in enumerate(self.headers):
            self.create_cell(self.table_frame, header, 0, col, font_size=15)

        # Add student data
        self.refresh_table()

        # Make columns and rows expandable
        for col in range(len(self.headers)):
            self.table_frame.grid_columnconfigure(col, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)

        # Bind the mouse wheel to scroll the canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    
    def on_entry_click(self, event):
        if self.search_entry.get() == "Rechercher un étudiant":
            self.search_entry.delete(0, "end")
            self.search_entry.insert(0, '')
            self.search_entry.config(fg='black')

    def on_focus_out(self, event):
        if self.search_entry.get() == '':
            self.search_entry.insert(0, "Rechercher un étudiant")
            self.search_entry.config(fg='grey')

    def create_cell(self, parent, text, row, column, width=11, height=3, font_size=12):
        cell = Tk.Label(parent, text=text, borderwidth=1, relief="solid", width=width, height=height, font=("Helvetica", font_size))
        cell.grid(row=row, column=column, sticky="nsew")
        return cell

    def create_action_buttons(self, parent, row, student_id):
        action_frame = Tk.Frame(parent)
        action_frame.grid(row=row, column=len(self.headers) - 1, sticky="nsew")

        edit_button = Tk.Button(action_frame, text="Modifier", bg="#FFD700", command=lambda r=row: self.app.grades_record(student_id))
        edit_button.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=True)

        delete_button = Tk.Button(action_frame, text="Supprimer", bg="#FF4C4C", command=lambda r=row: self.delete_student(student_id))
        delete_button.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=True)

    def refresh_table(self):
        # Clear the current table
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Add headers again
        for col, header in enumerate(self.headers):
            self.create_cell(self.table_frame, header, 0, col, font_size=15)

        # Add student data
        for row, student in enumerate(self.app.students, start=1):
            self.create_cell(self.table_frame, student["id"], row, 0)
            self.create_cell(self.table_frame, student["name"], row, 1)
            self.create_cell(self.table_frame, student["class"], row, 2)
            self.create_cell(self.table_frame, student["Analysis"], row, 3)
            self.create_cell(self.table_frame, student["Algebra"], row, 4)
            self.create_cell(self.table_frame, student["Algorithm"], row, 5)
            self.create_cell(self.table_frame, student["English"], row, 6)
            self.create_cell(self.table_frame, student["Mathematics"], row, 7)
            self.create_cell(self.table_frame, student["Physics"], row, 8)
            self.create_cell(self.table_frame, student["Chemistry"], row, 9)
            self.create_cell(self.table_frame, student["Biology"], row, 10)
            self.create_cell(self.table_frame, student["Arts"], row, 11)
            self.create_cell(self.table_frame, student["Informatique"], row, 12)
            self.create_cell(self.table_frame, student["Moyenne"], row, 13)
            self.create_action_buttons(self.table_frame, row, student["id"])

    def delete_student(self, student_id):
        result = messagebox.askquestion("Confirmation", "Are you sure you want to delete this student?", icon='warning')
        if result == 'yes':
            self.app.delete_student(student_id)
            self.refresh_table()

    def search_student(self):
        query = self.search_var.get().strip().lower()
        
        if not query:
            # Afficher un message d'erreur si le champ de recherche est vide
            messagebox.showinfo("Erreur", "Veuillez entrer un ID, un nom ou une classe.")
            return
        
        results_found = False
        for row, student in enumerate(self.app.students, start=1):
            # Recherche basée sur ID, nom ou classe
            if (query in str(student.get("id", "")).lower() or
                query in str(student.get("name", "")).lower() or
                query in str(student.get("class", "")).lower()):
                
                # Colorer les cellules en jaune si une correspondance est trouvée
                for col in range(len(student.values())):
                    self.table_frame.grid_slaves(row=row, column=col)[0].config(bg="yellow")
                results_found = True
            else:
                # Réinitialiser la couleur des cellules
                for col in range(len(student.values())):
                    self.table_frame.grid_slaves(row=row, column=col)[0].config(bg="white")
        
        if not results_found:
            # Afficher un message si aucun résultat n'est trouvé
            messagebox.showinfo("No matches", "No result founds.")
            
# Fonctionnalities

class StudentApp:
    def __init__(self):
        self.home = CTk.CTk()
        self.login_page()
        self.students = []
        self.load_students()
        self.student_record_app = None


    def generate_id(self):
        if not self.students:
            return "BS0001"
        last_id = self.students[-1]["id"]
        new_id_number = int(last_id[2:]) + 1
        return f"BS{new_id_number:04d}"
    
# JSON Parts

    def save_student(self):
        student_data = {
            "id": self.champ0.get(),
            "name": self.champ3.get(),
            "class": self.champ4.get(),
            "Analysis": 0, 
            "Algebra": 0, 
            "Algorithm": 0,
            "English": 0,
            "Mathematics": 0,
            "Physics": 0,
            "Chemistry": 0, 
            "Biology": 0, 
            "Arts": 0, 
            "Informatique": 0,
            "Moyenne": 0
            
        }
        self.students.append(student_data)
        self.save_students()
        messagebox.showinfo("Info","The student has been saved")
        self.student_record.destroy()
        self.refresh_table_after_add() 
    
    def save_students(self):
        with open("students.json", "w") as file:
            json.dump(self.students, file)

    def load_students(self):
        try:
            with open("students.json", "r") as file:
                self.students = json.load(file)
        except FileNotFoundError:
        
            with open("students.json", "w") as file:
                json.dump([], file)
    
    def delete_student(self, student_id):
       self.students = [student for student in self.students if student["id"] != student_id]
       self.save_students()

    def validate_number(self, value):
        pattern = re.compile(r'^\d+(\.\d{1,2})?$')
        if pattern.match(value):
            num = float(value)
            return 0 <= num <= 20
        return False

    def update_student(self, student_id):
        student = next((s for s in self.students if s["id"] == student_id), None)
        if student:
            try:
                if all([self.validate_number(self.champ8.get()) and self.validate_number(self.champ9.get()) and
                       self.validate_number(self.champ10.get()) and self.validate_number(self.champ5.get()) and
                       self.validate_number(self.champ6.get()) and self.validate_number(self.champ11.get()) and
                       self.validate_number(self.champ12.get()) and self.validate_number(self.champ13.get()) and
                       self.validate_number(self.champ14.get()) and self.validate_number(self.champ15.get())]):
                    
                    student["id"] = self.champ00.get()
                    student["name"] = self.champ03.get()
                    student["class"] = self.champ04.get()
                    student["Analysis"] = float(self.champ8.get())
                    student["Algebra"] = float(self.champ9.get())
                    student["Algorithm"] = float(self.champ10.get())
                    student["English"] = float(self.champ5.get())
                    student["Mathematics"] = float(self.champ6.get())
                    student["Physics"] = float(self.champ11.get())
                    student["Chemistry"] = float(self.champ12.get())
                    student["Biology"] = float(self.champ13.get())
                    student["Arts"] = float(self.champ14.get())
                    student["Informatique"] = float(self.champ15.get())
                    student["Moyenne"] = self.calculate_average(student)
                    
                    self.save_students()
                    messagebox.showinfo("Info", "The student data have been updated")
                    self.grade_record.destroy()
                    self.refresh_table_after_add()
                else:
                    messagebox.showerror("Error", "Veuillez entrer des nombres valides (entiers ou avec deux chiffres après la virgule) pour toutes les notes, compris entre 0 et 20.")
                    self.grade_record.destroy()

            except ValueError:
                messagebox.showerror("Error", "Veuillez entrer des nombres valides pour toutes les notes.")
                self.grade_record.destroy()

        else:
            messagebox.showerror("Error", "Étudiant non trouvé")
            self.grade_record.destroy()



    def toggle_password_visibility(self):
        if self.show_password.get():
            self.champ2.configure(show="")
        else:
            self.champ2.configure(show="*")

    def login_page(self):
        self.home.geometry("1200x800")
        CTk.set_appearance_mode("dark")
        CTk.set_default_color_theme("dark-blue")
        self.home.grid_rowconfigure(0, weight=1)
        self.home.grid_columnconfigure(0, weight=1)
        self.home.resizable(width=True, height=True)

        self.frame = CTk.CTkFrame(master=self.home, border_color="#C9C9C9", border_width=5)
        #self.frame.grid(row=0, column=0, padx=20, pady=50, sticky="nsew")
        self.frame.pack(pady=80, ipady=25, ipadx=15)
        
        self.title = CTk.CTkLabel(master=self.frame, text="Sign in", font=("Helvetica", 40, "bold"), text_color="#FFFFFF")
        self.title.pack(pady=20, padx=15)
        self.title.pack_propagate(False)
        
        self.champ1 = CTk.CTkEntry(master=self.frame, placeholder_text="Username", width=350, height=40, font=("Helvetica", 20))
        self.champ1.pack(pady= 20, padx=10)
        
        self.champ2 = CTk.CTkEntry(master=self.frame, placeholder_text="Password", show="*", width=350, height=40, font=("Helvetica", 20))
        self.champ2.pack(pady=20, padx=10)

        self.show_password = CTk.BooleanVar()
        show_password_checkbox = CTk.CTkCheckBox(master=self.frame, text="Show password", variable=self.show_password, command=self.toggle_password_visibility)
        show_password_checkbox.pack(pady=5)

        self.button1 = CTk.CTkButton(master=self.frame, text="Log in", hover_color="#0F968C", font=("Helvetica", 25, "bold"), command=self.login)
        self.button1.pack(pady=30, padx=10, ipady= 20, ipadx = 30)

    def show_student_records(self):
        self.clear_window()
        self.student_record_app = StudentRecordApp(self.home, self)
        self.home.mainloop()

    def login(self):
        self.username = self.champ1.get()
        self.password = self.champ2.get()

        if self.username == "admin" and self.password == "admin":
            self.show_student_records()

        elif self.username == "" and self.password == "":
            messagebox.showinfo("Info", "Please enter your name and your password")
            
        else:
            messagebox.showerror("Error", "Incorrect username or password")
            self.champ1.delete(0, "end")
            self.champ2.delete(0, "end")
            

    def student_record_page(self):
        self.student_record = CTk.CTk()
        self.student_record.geometry("1200x600")
        CTk.set_appearance_mode("dark")
        CTk.set_default_color_theme("dark-blue")
        self.student_record.grid_rowconfigure(0, weight=1)
        self.student_record.grid_columnconfigure(0, weight=1)
        self.student_record.resizable(width=True, height=True)

        self.frame1 = CTk.CTkFrame(master=self.student_record, border_width=3)
        self.frame1.pack(padx=10, pady=50)

        label_0 = CTk.CTkLabel(master=self.frame1, text="Add a student", font=("Helvetica", 40, "bold"))
        label_0.grid(row=0, column=0, columnspan=2, pady=18, padx=10)

        self.label1 = CTk.CTkLabel(master=self.frame1, text="ID number", font=("Helvetica", 18))
        self.label1.grid(row=1, column=0, pady=18, sticky="e")
        self.champ0 = CTk.CTkEntry(master=self.frame1, width=250, height=30, font=("Helvetica", 18))
        self.champ0.insert(0, self.generate_id())
        self.champ0.configure(state="readonly")
        self.champ0.grid(row=1, column=1, pady=20, padx=10, sticky="w")

        self.label_3 = CTk.CTkLabel(master=self.frame1, text="Name", font=("Helvetica",18))
        self.label_3.grid(row=2, column=0, pady=18, padx=10, sticky="e")
        self.champ3 = CTk.CTkEntry(master=self.frame1, width=250, height=30, font=("Helvetica", 18))
        self.champ3.grid(row=2, column=1, pady=20, padx=10, sticky="w")

        self.label_4 = CTk.CTkLabel(master=self.frame1, text="Class", font=("Helvetica",18))
        self.label_4.grid(row=3, column=0, pady=18, padx=10, sticky="e")
        self.champ4 = CTk.CTkComboBox(master=self.frame1, width=250, height=30, font=("Helvetica", 18), values=["CS25","EE25","ME25"])
        self.champ4.grid(row=3, column=1, pady=20, padx=10, sticky="w")

        # Save button outside of the frame1
        self.button3 = CTk.CTkButton(master=self.frame1, text="Save", hover_color="#0F968C", font=("Helvetica", 25, "bold"), command=self.save_student)
        self.button3.grid(pady=30, padx=100, ipady=10, ipadx=10)
        self.student_record.mainloop()

    
    def grades_record(self, student_id):
        student = next((student for student in self.students if student["id"] == student_id), None)
        if student:
            self.grade_record = CTk.CTk()
            self.grade_record.geometry("1200x600")
            CTk.set_appearance_mode("dark")
            CTk.set_default_color_theme("dark-blue")
            self.grade_record.grid_rowconfigure(0, weight=1)
            self.grade_record.grid_columnconfigure(0, weight=1)
            self.grade_record.resizable(width=True, height=True)

            label_0 = CTk.CTkLabel(master=self.grade_record, text="Edit student information", font=("Helvetica", 40, "bold"))
            label_0.grid(row=0, column=0, columnspan=2, pady=20, padx=10)

            # Frame for adding a student (left side)
            self.frame_left = CTk.CTkFrame(master=self.grade_record)
            self.frame_left.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

            self.label1 = CTk.CTkLabel(master=self.frame_left, text="ID number", font=("Helvetica", 18))
            self.label1.grid(row=1, column=0, pady=18, padx=10, sticky="e")
            self.champ00 = CTk.CTkEntry(master=self.frame_left, width=250, height=30, font=("Helvetica", 18))
            self.champ00.insert(0, student["id"])
            self.champ00.configure(state="readonly")
            self.champ00.grid(row=1, column=1, pady=18, padx=10, sticky="w")
            
            self.label_3 = CTk.CTkLabel(master=self.frame_left, text="Name", font=("Helvetica", 18))
            self.label_3.grid(row=2, column=0, pady=18, padx=10, sticky="e")
            self.champ03 = CTk.CTkEntry(master=self.frame_left, width=250, height=30, font=("Helvetica", 18))
            self.champ03.grid(row=2, column=1, pady=18, padx=10, sticky="w")
            self.champ03.insert(0, student["name"])

            self.label_4 = CTk.CTkLabel(master=self.frame_left, text="Class", font=("Helvetica", 18))
            self.label_4.grid(row=3, column=0, pady=18, padx=10, sticky="e")
            self.champ04 = CTk.CTkComboBox(master=self.frame_left, width=250, height=30, font=("Helvetica", 18), values=["CS25", "EE25", "ME25"])
            self.champ04.grid(row=3, column=1, pady=18, padx=10, sticky="w")
            self.champ04.set(student["class"])

            # Frame for grades (right side)
            self.frame_right = CTk.CTkFrame(master=self.grade_record)
            self.frame_right.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

            label_7 = CTk.CTkLabel(master=self.frame_right, text="Marks", font=("Helvetica", 40, "bold"), text_color="#FFFFFF")
            label_7.grid(row=0, column=0, columnspan=4, pady=20, padx=10)

            self.label8 = CTk.CTkLabel(master=self.frame_right, text="Analysis", font=("Helvetica", 18), text_color="#FFFFFF")
            self.label8.grid(row=1, column=0, pady=18, padx=10)
            self.champ8 = CTk.CTkEntry(master=self.frame_right, width=250, height=30, font=("Helvetica", 18))
            self.champ8.grid(row=1, column=1, pady=18, padx=10, sticky="w")
            self.champ8.insert(0, student["Analysis"])

            self.label9 = CTk.CTkLabel(master=self.frame_right, text="Algebra", font=("Helvetica", 18), text_color="#FFFFFF")
            self.label9.grid(row=2, column=0, pady=18, padx=10)
            self.champ9 = CTk.CTkEntry(master=self.frame_right, width=250, height=30, font=("Helvetica", 18))
            self.champ9.grid(row=2, column=1, pady=18, padx=10, sticky="w")
            self.champ9.insert(0, student["Algebra"])

            self.label10 = CTk.CTkLabel(master=self.frame_right, text="Algorithm", font=("Helvetica", 18), text_color="#FFFFFF")
            self.label10.grid(row=3, column=0, pady=18, padx=10)
            self.champ10 = CTk.CTkEntry(master=self.frame_right, width=250, height=30, font=("Helvetica", 18))
            self.champ10.grid(row=3, column=1, pady=18, padx=10, sticky="w")
            self.champ10.insert(0, student["Algorithm"])

            self.label_5 = CTk.CTkLabel(master=self.frame_right, text="English", font=("Helvetica", 18), text_color="#FFFFFF")
            self.label_5.grid(row=4, column=0, pady=18, padx=10, sticky="e")
            self.champ5 = CTk.CTkEntry(master=self.frame_right, width=250, height=30, font=("Helvetica", 18))
            self.champ5.grid(row=4, column=1, pady=18, padx=10, sticky="w")
            self.champ5.insert(0, student["English"])

            self.label_6 = CTk.CTkLabel(master=self.frame_right, text="Mathematics", font=("Helvetica", 18), text_color="#FFFFFF")
            self.label_6.grid(row=5, column=0, pady=18, padx=10, sticky="e")
            self.champ6 = CTk.CTkEntry(master=self.frame_right, width=250, height=30, font=("Helvetica", 18))
            self.champ6.grid(row=5, column=1, pady=18, padx=10, sticky="w")
            self.champ6.insert(0, student["Mathematics"])

            self.label11 = CTk.CTkLabel(master=self.frame_right, text="Physics", font=("Helvetica", 18), text_color="#FFFFFF")
            self.label11.grid(row=1, column=2, pady=18, padx=10)
            self.champ11 = CTk.CTkEntry(master=self.frame_right, width=250, height=30, font=("Helvetica", 18))
            self.champ11.grid(row=1, column=3, pady=18, padx=10, sticky="w")
            self.champ11.insert(0, student["Physics"])

            self.label12 = CTk.CTkLabel(master=self.frame_right, text="Chemistry", font=("Helvetica", 18), text_color="#FFFFFF")
            self.label12.grid(row=2, column=2, pady=18, padx=10)
            self.champ12 = CTk.CTkEntry(master=self.frame_right, width=250, height=30, font=("Helvetica", 18))
            self.champ12.grid(row=2, column=3, pady=18, padx=10, sticky="w")
            self.champ12.insert(0, student["Chemistry"])

            self.label13 = CTk.CTkLabel(master=self.frame_right, text="Biology", font=("Helvetica", 18), text_color="#FFFFFF")
            self.label13.grid(row=3, column=2, pady=18, padx=10)
            self.champ13 = CTk.CTkEntry(master=self.frame_right, width=250, height=30, font=("Helvetica", 18))
            self.champ13.grid(row=3, column=3, pady=18, padx=10, sticky="w")
            self.champ13.insert(0, student["Biology"])

            self.label_14 = CTk.CTkLabel(master=self.frame_right, text="Arts", font=("Helvetica", 18), text_color="#FFFFFF")
            self.label_14.grid(row=4, column=2, pady=18, padx=10, sticky="e")
            self.champ14 = CTk.CTkEntry(master=self.frame_right, width=250, height=30, font=("Helvetica", 18))
            self.champ14.grid(row=4, column=3, pady=18, padx=10, sticky="w")
            self.champ14.insert(0, student["Arts"])

            self.label_15 = CTk.CTkLabel(master=self.frame_right, text="Informatique", font=("Helvetica", 18), text_color="#FFFFFF")
            self.label_15.grid(row=5, column=2, pady=18, padx=10, sticky="e")
            self.champ15 = CTk.CTkEntry(master=self.frame_right, width=250, height=30, font=("Helvetica", 18))
            self.champ15.grid(row=5, column=3, pady=18, padx=10, sticky="w")
            self.champ15.insert(0, student["Informatique"])

            self.button2 = CTk.CTkButton(master=self.grade_record, text="Save", hover_color="#0F968C", font=("Helvetica", 25, "bold"), command=lambda: self.update_student(student_id))
            self.button2.grid(row=2, column=1, columnspan=2, pady=30, padx=10, ipady=10, ipadx=10)

            self.button3 = CTk.CTkButton(master=self.grade_record, text="Retour", hover_color="#0F968C", font=("Helvetica", 25, "bold"), command=self.grade_record.destroy)
            self.button3.grid(row=2, column=0, columnspan=2, pady=30, padx=10, ipady=10, ipadx=10)

            self.grade_record.mainloop()

    def clear_window(self):
        for widget in self.home.winfo_children():
            widget.destroy()

    def refresh_table_after_add(self):
        if self.student_record_app:
            self.student_record_app.refresh_table()

    def calculate_average(self, student):
        subjects = ["Analysis", "Algebra", "Algorithm", "English", "Mathematics", "Physics", "Chemistry", "Biology", "Arts", "Informatique"]
        total = sum(student[subject] for subject in subjects)
        return round(total / len(subjects), 2)


if __name__ == "__main__":
    app = StudentApp()
    app.home.mainloop()