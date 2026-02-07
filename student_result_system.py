"""
Student Result Management System
Part 2 - Foundations of Programming Assignment
EduTech Solutions
Developer: [Your Name]
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ============================================
# STUDENT CLASS DEFINITION
# ============================================
class Student:
    
    def __init__(self, student_id, name):
        """
        Initialize a student object.
        
        Args:
            student_id (int): Unique student identifier
            name (str): Student's full name
        """
        self.student_id = student_id      # Integer
        self.name = name                  # String
        self.marks = {}                   # Dictionary {subject: mark}
        self.total_marks = 0.0            # Float
        self.percentage = 0.0             # Float
        self.grade = ''                   # String
    
    def calculate_results(self):
        """Calculate total marks, percentage, and assign final grade."""
        
        # If no marks, set defaults
        if not self.marks:
            self.total_marks = 0.0
            self.percentage = 0.0
            self.grade = 'N/A'
            return
        
        # Calculate total marks from all subjects
        self.total_marks = sum(self.marks.values())
        
        # Calculate percentage (each subject out of 100)
        total_subjects = len(self.marks)
        max_possible_marks = total_subjects * 100
        if max_possible_marks > 0:
            self.percentage = (self.total_marks / max_possible_marks) * 100
        else:
            self.percentage = 0.0
        
        # Assign grade based on percentage
        if self.percentage >= 90:
            self.grade = 'A'
        elif self.percentage >= 80:
            self.grade = 'B'
        elif self.percentage >= 70:
            self.grade = 'C'
        elif self.percentage >= 60:
            self.grade = 'D'
        else:
            self.grade = 'F'  # Below 60%


# ============================================
# MAIN APPLICATION CLASS
# ============================================
class ResultManagementSystem:
    """Main GUI application for managing student results."""
    
    def __init__(self, root):
        """
        Initialize the main application window.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("EduTech Solutions - Student Result System")
        self.root.geometry("1000x700")
        
        # Configure grid weights for resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Data storage
        self.students = {}  # Dictionary: {student_id: Student object}
        self.subjects = ['Mathematics', 'Science', 'English', 'History', 'Computer Science']
        self.data_file = "student_data.json"
        
        # Load existing data if available
        self.load_from_file()
        
        # Create GUI components
        self.create_widgets()
        
        # Refresh student list display
        self.refresh_student_list()
    
    # ============================================
    # GUI CREATION METHODS
    # ============================================
    def create_widgets(self):
        """Create and arrange all GUI components."""
        
        # Main container frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Title Label
        title_label = ttk.Label(
            main_frame, 
            text="🎓 Student Result Management System",
            font=('Arial', 18, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=tk.W)
        
        # ========== LEFT PANEL: Input Form ==========
        input_frame = ttk.LabelFrame(main_frame, text="Student Information", padding="15")
        input_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W), padx=(0, 10))
        
        # Student ID
        ttk.Label(input_frame, text="Student ID:", font=('Arial', 10)).grid(
            row=0, column=0, sticky=tk.W, pady=(0, 8))
        self.id_var = tk.StringVar()
        id_entry = ttk.Entry(input_frame, textvariable=self.id_var, width=25, font=('Arial', 10))
        id_entry.grid(row=0, column=1, pady=(0, 8), padx=(10, 0))
        
        # Student Name
        ttk.Label(input_frame, text="Student Name:", font=('Arial', 10)).grid(
            row=1, column=0, sticky=tk.W, pady=(0, 8))
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(input_frame, textvariable=self.name_var, width=25, font=('Arial', 10))
        name_entry.grid(row=1, column=1, pady=(0, 8), padx=(10, 0))
        
        # Marks Entry for each subject
        ttk.Label(input_frame, text="\nSubject Marks (0-100):", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        self.marks_vars = {}
        for i, subject in enumerate(self.subjects):
            ttk.Label(input_frame, text=f"{subject}:", font=('Arial', 9)).grid(
                row=i+3, column=0, sticky=tk.W, pady=3)
            var = tk.StringVar()
            entry = ttk.Entry(input_frame, textvariable=var, width=20, font=('Arial', 9))
            entry.grid(row=i+3, column=1, pady=3, padx=(10, 0))
            self.marks_vars[subject] = var
        
        # Action Buttons Frame
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=len(self.subjects)+3, column=0, columnspan=2, pady=(20, 0))
        
        # Add Student Button
        add_btn = ttk.Button(
            button_frame, 
            text="➕ Add Student", 
            command=self.add_student,
            width=15
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Calculate Grade Button
        calc_btn = ttk.Button(
            button_frame, 
            text="📊 Calculate Grade", 
            command=self.calculate_grade,
            width=15
        )
        calc_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear Form Button
        clear_btn = ttk.Button(
            button_frame, 
            text="🗑️ Clear Form", 
            command=self.clear_form,
            width=15
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # ========== RIGHT PANEL: Student Records Table ==========
        table_frame = ttk.LabelFrame(main_frame, text="Student Records", padding="15")
        table_frame.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Create Treeview (table) with columns
        columns = ('ID', 'Name', 'Total', 'Percentage', 'Grade')
        self.tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show='headings',
            height=20,
            selectmode='browse'
        )
        
        # Define column headings and widths
        column_widths = {'ID': 80, 'Name': 150, 'Total': 80, 'Percentage': 100, 'Grade': 80}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col], anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout for tree and scrollbar
        self.tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_student_select)
        
        # ========== BOTTOM PANEL: System Controls ==========
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        # Control buttons
        buttons = [
            ("📋 View All Results", self.view_all_results),
            ("💾 Save Records", self.save_to_file),
            ("📂 Load Records", self.load_from_file),
            ("❌ Exit", self.exit_program)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(control_frame, text=text, command=command, width=15)
            btn.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(
            main_frame, 
            text=f"Total Students: {len(self.students)}",
            font=('Arial', 9, 'italic')
        )
        self.status_label.grid(row=3, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)
    
    # ============================================
    # CORE FUNCTIONALITY METHODS
    # ============================================
    def add_student(self):
        """Add a new student record from form data."""
        
        # Get and validate student ID
        student_id_str = self.id_var.get().strip()
        if not student_id_str:
            messagebox.showwarning("Missing Information", "Please enter a Student ID!")
            return
        
        if not student_id_str.isdigit():
            messagebox.showwarning("Invalid Input", "Student ID must be a number!")
            return
        
        student_id = int(student_id_str)
        
        # Check for duplicate ID
        if student_id in self.students:
            messagebox.showwarning(
                "Duplicate ID", 
                f"Student ID {student_id} already exists!\nPlease use a different ID."
            )
            return
        
        # Get and validate student name
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Missing Information", "Please enter a Student Name!")
            return
        
        # Create new student object
        new_student = Student(student_id, name)
        
        # Collect and validate marks
        marks_entered = False
        for subject in self.subjects:
            mark_str = self.marks_vars[subject].get().strip()
            
            if mark_str:  # If mark is provided
                try:
                    mark = float(mark_str)
                    
                    # Validate mark range (0-100)
                    if mark < 0 or mark > 100:
                        messagebox.showwarning(
                            "Invalid Mark", 
                            f"Mark for {subject} must be between 0 and 100!"
                        )
                        return
                    
                    new_student.marks[subject] = mark
                    marks_entered = True
                    
                except ValueError:
                    messagebox.showwarning(
                        "Invalid Input", 
                        f"Mark for {subject} must be a number!"
                    )
                    return
        
        # If no marks entered, show warning but allow creation
        if not marks_entered:
            response = messagebox.askyesno(
                "No Marks Entered", 
                "No marks entered for this student. Create student without marks?"
            )
            if not response:
                return
        
        # Add student to collection
        self.students[student_id] = new_student
        
        # Calculate initial results
        new_student.calculate_results()
        
        # Update display
        self.refresh_student_list()
        
        # Show success message
        messagebox.showinfo(
            "Success", 
            f"Student added successfully!\n\n"
            f"ID: {student_id}\n"
            f"Name: {name}\n"
            f"Grade: {new_student.grade}"
        )
        
        # Clear form for next entry
        self.clear_form()
    
    def calculate_grade(self):
        """Calculate and display grade for a student."""
        
        # Get student ID
        student_id_str = self.id_var.get().strip()
        if not student_id_str:
            messagebox.showwarning("Missing Information", "Please enter a Student ID!")
            return
        
        if not student_id_str.isdigit():
            messagebox.showwarning("Invalid Input", "Student ID must be a number!")
            return
        
        student_id = int(student_id_str)
        
        # Check if student exists
        if student_id not in self.students:
            messagebox.showwarning(
                "Student Not Found", 
                f"Student with ID {student_id} not found!\n"
                f"Please add the student first or load existing records."
            )
            return
        
        # Get student and calculate results
        student = self.students[student_id]
        student.calculate_results()
        
        # Prepare result message
        result_message = f"📊 **Student Results Summary**\n\n"
        result_message += f"Student ID: {student_id}\n"
        result_message += f"Name: {student.name}\n\n"
        
        if student.marks:
            result_message += "Subject Marks:\n"
            for subject, mark in student.marks.items():
                result_message += f"  • {subject}: {mark}/100\n"
            result_message += f"\nTotal Marks: {student.total_marks:.1f}/500\n"
        else:
            result_message += "No marks recorded.\n\n"
        
        result_message += f"Percentage: {student.percentage:.1f}%\n"
        result_message += f"Final Grade: {student.grade}\n"
        
        # Display results
        messagebox.showinfo("Grade Calculation Results", result_message)
        
        # Update display
        self.refresh_student_list()
    
    def view_all_results(self):
        """Display detailed view of all student results."""
        
        if not self.students:
            messagebox.showinfo("No Records", "No student records available.")
            return
        
        # Create new window for detailed results
        results_window = tk.Toplevel(self.root)
        results_window.title("📄 All Student Results - Detailed View")
        results_window.geometry("800x500")
        
        # Title
        title_label = ttk.Label(
            results_window, 
            text="📋 Complete Student Results Report",
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=(10, 20))
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(results_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert report header
        text_widget.insert(tk.END, "=" * 70 + "\n")
        text_widget.insert(tk.END, "STUDENT RESULTS REPORT\n")
        text_widget.insert(tk.END, f"Generated: {len(self.students)} students\n")
        text_widget.insert(tk.END, "=" * 70 + "\n\n")
        
        # Insert each student's detailed results
        for student_id in sorted(self.students.keys()):
            student = self.students[student_id]
            student.calculate_results()  # Ensure calculations are current
            
            text_widget.insert(tk.END, f"Student ID: {student_id}\n")
            text_widget.insert(tk.END, f"Name: {student.name}\n")
            
            if student.marks:
                text_widget.insert(tk.END, "Subject Marks:\n")
                for subject, mark in student.marks.items():
                    text_widget.insert(tk.END, f"  • {subject}: {mark}/100\n")
                text_widget.insert(tk.END, f"Total Marks: {student.total_marks:.1f}/500\n")
            else:
                text_widget.insert(tk.END, "No marks recorded.\n")
            
            text_widget.insert(tk.END, f"Percentage: {student.percentage:.1f}%\n")
            text_widget.insert(tk.END, f"Final Grade: {student.grade}\n")
            text_widget.insert(tk.END, "-" * 50 + "\n\n")
        
        # Make text widget read-only
        text_widget.configure(state='disabled')
        
        # Close button
        close_btn = ttk.Button(
            results_window, 
            text="Close Report", 
            command=results_window.destroy
        )
        close_btn.pack(pady=(0, 10))
    
    # ============================================
    # FILE HANDLING METHODS
    # ============================================
    def save_to_file(self):
        """Save all student records to JSON file."""
        
        if not self.students:
            messagebox.showwarning("No Data", "No student records to save!")
            return
        
        try:
            # Prepare data for JSON serialization
            data_to_save = {}
            for student_id, student in self.students.items():
                data_to_save[student_id] = {
                    'name': student.name,
                    'marks': student.marks,
                    'total_marks': student.total_marks,
                    'percentage': student.percentage,
                    'grade': student.grade
                }
            
            # Write to file
            with open(self.data_file, 'w') as file:
                json.dump(data_to_save, file, indent=4, sort_keys=True)
            
            # Update status
            self.status_label.config(text=f"Data saved! Total Students: {len(self.students)}")
            
            messagebox.showinfo(
                "Save Successful", 
                f"All student records saved successfully!\n"
                f"File: {self.data_file}\n"
                f"Students saved: {len(self.students)}"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Save Error", 
                f"Failed to save data:\n{str(e)}"
            )
    
    def load_from_file(self):
        """Load student records from JSON file."""
        
        try:
            if not os.path.exists(self.data_file):
                messagebox.showinfo(
                    "No Data File", 
                    f"No saved data found.\nFile '{self.data_file}' doesn't exist.\n"
                    f"Please save some data first."
                )
                return
            
            # Read from file
            with open(self.data_file, 'r') as file:
                loaded_data = json.load(file)
            
            # Clear current students
            self.students.clear()
            
            # Recreate Student objects from loaded data
            for student_id_str, student_data in loaded_data.items():
                student_id = int(student_id_str)
                student = Student(student_id, student_data['name'])
                student.marks = student_data['marks']
                student.total_marks = student_data['total_marks']
                student.percentage = student_data['percentage']
                student.grade = student_data['grade']
                self.students[student_id] = student
            
            # Update display
            self.refresh_student_list()
            
            # Update status
            self.status_label.config(text=f"Data loaded! Total Students: {len(self.students)}")
            
            messagebox.showinfo(
                "Load Successful", 
                f"Student records loaded successfully!\n"
                f"File: {self.data_file}\n"
                f"Students loaded: {len(self.students)}"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Load Error", 
                f"Failed to load data:\n{str(e)}"
            )
    
    # ============================================
    # UTILITY METHODS
    # ============================================
    def refresh_student_list(self):
        """Update the treeview with current student data."""
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert current students (sorted by ID)
        for student_id in sorted(self.students.keys()):
            student = self.students[student_id]
            
            # Ensure calculations are current
            student.calculate_results()
            
            # Insert into treeview
            self.tree.insert('', 'end', values=(
                student_id,
                student.name,
                f"{student.total_marks:.1f}",
                f"{student.percentage:.1f}%",
                student.grade
            ))
        
        # Update status label
        self.status_label.config(text=f"Total Students: {len(self.students)}")
    
    def on_student_select(self, event):
        """Load selected student's data into the form when clicked in table."""
        
        selection = self.tree.selection()
        if selection:
            # Get selected item data
            item = self.tree.item(selection[0])
            student_id = int(item['values'][0])
            
            # Check if student exists in dictionary
            if student_id in self.students:
                student = self.students[student_id]
                
                # Load data into form
                self.id_var.set(str(student_id))
                self.name_var.set(student.name)
                
                # Clear all marks first
                for subject in self.subjects:
                    self.marks_vars[subject].set('')
                
                # Set marks for subjects that have values
                for subject, mark in student.marks.items():
                    if subject in self.marks_vars:
                        self.marks_vars[subject].set(str(mark))
    
    def clear_form(self):
        """Clear all input fields in the form."""
        
        self.id_var.set('')
        self.name_var.set('')
        for subject in self.subjects:
            self.marks_vars[subject].set('')
    
    def exit_program(self):
        """Exit the application with confirmation."""
        
        if self.students:
            response = messagebox.askyesnocancel(
                "Exit Program", 
                "Do you want to save student records before exiting?\n\n"
                "Yes: Save and Exit\n"
                "No: Exit without Saving\n"
                "Cancel: Return to Program"
            )
            
            if response is None:  # Cancel
                return
            elif response:  # Yes
                self.save_to_file()
        
        # Exit program
        self.root.quit()


# ============================================
# MAIN PROGRAM ENTRY POINT
# ============================================
def main():
    """Main entry point for the application."""
    
    # Create main window
    root = tk.Tk()
    
    # Create application instance
    app = ResultManagementSystem(root)
    
    # Start main event loop
    root.mainloop()


# ============================================
# PROGRAM EXECUTION
# ============================================
if __name__ == "__main__":
    main()