/*
================================================================================
Payroll Management System
Unit 05: Fundamentals of Programming - Part 1 Assignment
Company: JaneC Pvt. Ltd.
Developer: [Kaveesha Sewmini]
Date: [2026/01/26]
================================================================================
Description:
This program implements a complete payroll management system for JaneC Pvt. Ltd.
It allows HR staff to manage employee salaries, calculate taxes based on income
brackets, and maintain persistent employee records.
================================================================================
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/* ============================================================================
   1.1 DEFINE EMPLOYEE STRUCTURE
   This structure defines the data format for each employee record.
============================================================================ */
struct Employee {
    int emp_id;           // Unique employee ID (integer)
    char name[100];       // Employee's name (string)
    float basic_salary;   // Base salary amount (float)
    float tax;            // Tax deducted (float)
    float net_salary;     // Final salary after tax (float)
};

/* Global variables for employee management */
#define MAX_EMPLOYEES 100
struct Employee employees[MAX_EMPLOYEES];
int employee_count = 0;
const char *FILENAME = "employees.txt";

/* ============================================================================
   FUNCTION PROTOTYPES
   These declarations specify the functions available in the program.
============================================================================ */
float calculate_tax(float basic_salary);
void calculate_net_salary(struct Employee *e);
void add_employee();
void display_all_employees();
void display_employee_by_id(int emp_id);
void save_to_file();
void load_from_file();
void search_employee();
void display_menu();
void clear_input_buffer();

/* ============================================================================
   1.2 TAX CALCULATION FUNCTION
   This function implements the tax bracket logic specified. 
   It demonstrates control flow through if-else statements (LO1.4).
============================================================================ */
float calculate_tax(float basic_salary) {
    float tax_amount = 0.0;
    
    /* Decision structure for tax brackets */
    if (basic_salary < 10000.0) {
        tax_amount = 0.0;                     // No tax for salary < 10,000
    } 
    else if (basic_salary <= 30000.0) {
        tax_amount = basic_salary * 0.10;     // 10% tax bracket
    } 
    else if (basic_salary <= 50000.0) {
        tax_amount = basic_salary * 0.20;     // 20% tax bracket
    } 
    else {
        tax_amount = basic_salary * 0.30;     // 30% tax bracket
    }
    
    return tax_amount;
}

/* ============================================================================
   NET SALARY CALCULATION USING POINTERS
   This function calculates net salary after tax deduction.
   It uses pointers for efficient data access (LO1.3).
============================================================================ */
void calculate_net_salary(struct Employee *e) {
    e->tax = calculate_tax(e->basic_salary);
    e->net_salary = e->basic_salary - e->tax;
}

/* ============================================================================
   ADD EMPLOYEE FUNCTION
   This function allows users to add new employee records.
   It demonstrates data input and validation.
============================================================================ */
void add_employee() {
    if (employee_count >= MAX_EMPLOYEES) {
        printf("Maximum employee limit reached (%d)!\n", MAX_EMPLOYEES);
        return;
    }
    
    struct Employee new_emp;
    
    printf("\n=== ADD NEW EMPLOYEE ===\n");
    
    /* Get employee ID with validation */
    int id_exists;
    do {
        id_exists = 0;
        printf("Enter Employee ID: ");
        scanf("%d", &new_emp.emp_id);
        clear_input_buffer();
        
        /* Check if ID already exists */
        for (int i = 0; i < employee_count; i++) {
            if (employees[i].emp_id == new_emp.emp_id) {
                printf("Employee ID %d already exists! Please enter a different ID.\n", new_emp.emp_id);
                id_exists = 1;
                break;
            }
        }
    } while (id_exists);
    
    /* Get employee name */
    printf("Enter Employee Name: ");
    fgets(new_emp.name, sizeof(new_emp.name), stdin);
    new_emp.name[strcspn(new_emp.name, "\n")] = 0;  // Remove newline character
    
    /* Get basic salary with validation */
    printf("Enter Basic Salary: RS.");
    scanf("%f", &new_emp.basic_salary);
    clear_input_buffer();
    
    if (new_emp.basic_salary < 0) {
        printf("Warning: Salary cannot be negative! Setting to 0.\n");
        new_emp.basic_salary = 0;
    }
    
    /* Calculate tax and net salary */
    calculate_net_salary(&new_emp);
    
    /* Add to array */
    employees[employee_count] = new_emp;
    employee_count++;
    
    /* Display results */
    printf("\nEmployee added successfully!\n");
    printf("Tax deducted: Rs.%.2f\n", new_emp.tax);
    printf("Net Salary: Rs.%.2f\n", new_emp.net_salary);
    
    /* Save to file after every update */
    save_to_file();
}

/* ============================================================================
   1.3 DISPLAY EMPLOYEE BY ID USING POINTERS
   This function searches for an employee by ID and displays their details.
   It demonstrates pointer usage for array traversal (LO1.3).
============================================================================ */
void display_employee_by_id(int emp_id) {
    int found = 0;
    
    /* Search through array using pointer arithmetic */
    struct Employee *emp_ptr = employees;
    
    for (int i = 0; i < employee_count; i++, emp_ptr++) {
        if (emp_ptr->emp_id == emp_id) {
            printf("\n=== EMPLOYEE DETAILS ===\n");
            printf("Employee ID: %d\n", emp_ptr->emp_id);
            printf("Name: %s\n", emp_ptr->name);
            printf("Basic Salary: Rs.%.2f\n", emp_ptr->basic_salary);
            printf("Tax Deducted: Rs.%.2f\n", emp_ptr->tax);
            printf("Net Salary: Rs.%.2f\n", emp_ptr->net_salary);
            found = 1;
            break;
        }
    }
    
    if (!found) {
        printf("Employee with ID %d not found.\n", emp_id);
    }
}

/* ============================================================================
   SEARCH EMPLOYEE FUNCTION
   This function provides the user interface for searching employees.
============================================================================ */
void search_employee() {
    int emp_id;
    
    printf("\nEnter Employee ID to search: ");
    scanf("%d", &emp_id);
    clear_input_buffer();
    
    display_employee_by_id(emp_id);
}

/* ============================================================================
   DISPLAY ALL EMPLOYEES
   This function shows all employee records in a formatted table.
============================================================================ */
void display_all_employees() {
    if (employee_count == 0) {
        printf("\nNo employee records available.\n");
        return;
    }
    
    printf("\n=== ALL EMPLOYEE RECORDS ===\n");
    printf("Total Employees: %d\n", employee_count);
    printf("------------------------------------------------------------\n");
    printf("%-10s %-20s %-15s %-10s %-12s\n", 
           "ID", "Name", "Basic Salary", "Tax", "Net Salary");
    printf("------------------------------------------------------------\n");
    
    for (int i = 0; i < employee_count; i++) {
        printf("%-10d %-20s Rs.%-14.2f Rs.%-9.2f Rs.%-11.2f\n",
               employees[i].emp_id,
               employees[i].name,
               employees[i].basic_salary,
               employees[i].tax,
               employees[i].net_salary);
    }
    printf("------------------------------------------------------------\n");
}

/* ============================================================================
   1.4 FILE HANDLING FUNCTIONS
   These functions implement persistent data storage as required.
   They demonstrate file I/O operations in C.
============================================================================ */
void save_to_file() {
    FILE *file = fopen(FILENAME, "w");
    if (file == NULL) {
        printf("Error opening file '%s' for writing!\n", FILENAME);
        return;
    }
    
    /* Write employee count first */
    fprintf(file, "%d\n", employee_count);
    
    /* Write each employee record */
    for (int i = 0; i < employee_count; i++) {
        fprintf(file, "%d|%s|%.2f|%.2f|%.2f\n",
                employees[i].emp_id,
                employees[i].name,
                employees[i].basic_salary,
                employees[i].tax,
                employees[i].net_salary);
    }
    
    fclose(file);
    printf("Data saved to '%s' successfully.\n", FILENAME);
}

void load_from_file() {
    FILE *file = fopen(FILENAME, "r");
    if (file == NULL) {
        printf("No existing data file found. Starting fresh.\n");
        return;
    }
    
    /* Read employee count */
    fscanf(file, "%d\n", &employee_count);
    
    /* Read each employee record */
    for (int i = 0; i < employee_count; i++) {
        fscanf(file, "%d|%99[^|]|%f|%f|%f\n",
               &employees[i].emp_id,
               employees[i].name,
               &employees[i].basic_salary,
               &employees[i].tax,
               &employees[i].net_salary);
    }
    
    fclose(file);
    printf("Loaded %d employee records from '%s'.\n", employee_count, FILENAME);
}

/* ============================================================================
   UTILITY FUNCTIONS
   These functions support the main program operations.
============================================================================ */
void clear_input_buffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

void display_menu() {
    printf("\n=== PAYROLL MANAGEMENT SYSTEM ===\n");
    printf("1. Add New Employee\n");
    printf("2. Display All Employees\n");
    printf("3. Search Employee by ID\n");
    printf("4. Save Data to File\n");
    printf("5. Exit\n");
    printf("Enter your choice (1-5): ");
}

/* ============================================================================
   MAIN FUNCTION
   This is the entry point of the program.
   It demonstrates the overall program structure (LO1.2).
============================================================================ */
int main() {
    int choice;
    
    printf("=============================================\n");
    printf("   PAYROLL MANAGEMENT SYSTEM - JaneC Pvt. Ltd\n");
    printf("=============================================\n");
    
    /* Load existing data when program starts */
    load_from_file();
    
    /* Main program loop */
    do {
        display_menu();
        scanf("%d", &choice);
        clear_input_buffer();
        
        /* Execute user's choice */
        switch (choice) {
            case 1:
                add_employee();
                break;
            case 2:
                display_all_employees();
                break;
            case 3:
                search_employee();
                break;
            case 4:
                save_to_file();
                break;
            case 5:
                printf("\nSaving data before exit...\n");
                save_to_file();
                printf("Thank you for using Payroll System. Goodbye!\n");
                break;
            default:
                printf("Invalid choice! Please enter a number between 1 and 5.\n");
        }
        
        /* Pause for user to see results */
        if (choice != 5) {
            printf("\nPress Enter to continue...");
            getchar();
        }
        
    } while (choice != 5);
    
    return 0;
}