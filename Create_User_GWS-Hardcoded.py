import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import subprocess
import re

# List of departments available in our organization
DEPARTMENTS = ["Core Business", "Engineering Support", "Finance", "HR", "Legal", "Management", "Marketing", "Operations Domain", "Organizations Super Admins", "Sales"]

# Base groups for all users in a department
BASE_GROUPS = {
    "core business": ["account-management@deytech.se", "core-business-analytics@deytech.se", "core-business-operations@deytech.se", "customer-success@deytech.se"],
    "engineering support": ["engineering-support@deytech.se", "engineering@deytech.se", "devops@deytech.se"],
    "finance": ["finance-accounting@deytech.se", "finance-compliance@deytech.se", "finance-payroll@deytech.se", "compliance@deytech.se"],
    "hr": ["hr@deytech.se", "hr-recruitment@deytech.se", "hr-benefits@deytech.se"],
    "legal": ["legal-compliance@deytech.se", "legal-contracts@deytech.se", "compliance@deytech.se"],
    "management": ["strategic-management@deytech.se"],
    "marketing": ["marketing@deytech.se", "digital-marketing@deytech.se", "marketing-analytics@deytech.se"],
    "operations domain": ["project-management@deytech.se", "operations-it@deytech.se", "operations-supply-chain@deytech.se"],
    "organizations super admins": ["all-admin@deytech.se", "admin@deytech.se", "super-admins-security@deytech.se"],
    "sales": ["sales@deytech.se", "all-sales@deytech.se", "sales-operations@deytech.se"]
}

# Role-specific groups based on job title keywords
ROLE_GROUPS = {
    "core business": {"manager": "core-business-managers@deytech.se", "lead": "core-business-leadership@deytech.se", "director": "core-business-directors@deytech.se"},
    "engineering support": {"manager": "engineering-managers@deytech.se", "lead": "engineering-support-leadership@deytech.se", "director": "engineering-directors@deytech.se"},
    "finance": {"manager": "finance-managers@deytech.se", "lead": "finance-leadership@deytech.se", "director": "finance-directors@deytech.se"},
    "hr": {"manager": "hr-managers@deytech.se", "lead": "hr-leadership@deytech.se", "director": "hr-directors@deytech.se"},
    "legal": {"manager": "legal-managers@deytech.se", "lead": "legal-leadership@deytech.se", "director": "legal-directors@deytech.se"},
    "management": {"manager": "management-managers@deytech.se", "lead": "management-leads@deytech.se", "director": "management-directors@deytech.se"},
    "marketing": {"manager": "marketing-managers@deytech.se", "lead": "marketing-leadership@deytech.se", "director": "marketing-directors@deytech.se"},
    "operations domain": {"manager": "operations-managers@deytech.se", "lead": "operations-leadership@deytech.se", "director": "operations-directors@deytech.se"},
    "organizations super admins": {"manager": "super-admins-managers@deytech.se", "lead": "super-admins-leadership@deytech.se", "director": "super-admins-directors@deytech.se"},
    "sales": {"manager": "sales-managers@deytech.se", "lead": "sales-leadership@deytech.se", "director": "sales-directors@deytech.se"}
}

# Base groups for all users in a location
BASE_LOCATION_GROUPS = {
    "stockholm": ["stockholm-office@deytech.se", "stockholm-all@deytech.se", "stockholm-facilities@deytech.se", "stockholm-it@deytech.se", "stockholm-social@deytech.se"],
    "gothenburg": ["gothenburg-office@deytech.se", "gothenburg-all@deytech.se", "gothenburg-facilities@deytech.se", "gothenburg-itsupport@deytech.se", "gothenburg-social@deytech.se"],
    "remote": ["remote-team@deytech.se"]
}

# Role-specific location groups based on job title keywords
ROLE_LOCATION_GROUPS = {
    "stockholm": {"manager": "stockholm-management@deytech.se", "lead": "stockholm-management@deytech.se", "director": "stockholm-management@deytech.se"},
    "gothenburg": {"manager": "gothenburg-management@deytech.se", "lead": "gothenburg-management@deytech.se", "director": "gothenburg-management@deytech.se"}
}

# Groups that everyone should be added to regardless of department/location
DEFAULT_GROUPS = ["all-company@deytech.se", "announcements@deytech.se"]

def normalize_text(text):
    return text.lower().strip()

def generate_random_password(length=None):
    if length is None:
        length = random.randint(10, 12)
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Determines which groups a user should be added to based on department, location, and job title
def determine_groups_to_add(department, location, job_title):
    groups = set()
    dept_clean = normalize_text(department or "")
    location_clean = normalize_text(location or "")
    job_title_clean = normalize_text(job_title or "")
    
    # Add base department groups
    if dept_clean in BASE_GROUPS:
        groups.update(BASE_GROUPS[dept_clean])
    
    # Add role-specific department groups based on exact keyword match
    if dept_clean in ROLE_GROUPS:
        role_groups = ROLE_GROUPS[dept_clean]
        for keyword, group in role_groups.items():
            if re.search(r'\b' + re.escape(keyword) + r'\b', job_title_clean):
                groups.add(group)
    
    # Add base location groups
    for loc_key, loc_groups in BASE_LOCATION_GROUPS.items():
        if loc_key in location_clean:
            groups.update(loc_groups)
    
    # Add role-specific location groups based on exact keyword match
    for loc_key, role_groups in ROLE_LOCATION_GROUPS.items():
        if loc_key in location_clean:
            for keyword, group in role_groups.items():
                if re.search(r'\b' + re.escape(keyword) + r'\b', job_title_clean):
                    groups.add(group)
    
    # Add default groups that everyone gets
    groups.update(DEFAULT_GROUPS)
    
    return sorted(groups)

# Executes Google Admin SDK commands through GAM - our interface to Google Workspace
def run_gam_command(command_parts_list):
    command_to_run = ['gam'] + command_parts_list
    print(f"\nExecuting: {' '.join(command_to_run)}")
    try:
        process = subprocess.Popen(command_to_run, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            print("Success!")
            if stdout: print(stdout)
        else:
            print("Error!")
            if stderr: print(stderr)
            if stdout: print("Output:\n", stdout)
    except FileNotFoundError:
        print("GAM not found. Ensure GAM is installed and available in PATH.")
    except Exception as e:
        print(f"Unexpected error: {e}")

class UserCreatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Google Workspace User Creator Script: Author: Arber Celaj")
        root.geometry("640x460")
        root.resizable(False, False)
        
        # Create all the form fields for user input
        self.entries = {}
        for i, (label_text, var_name) in enumerate([
            ("Given Name", "given_name"),
            ("Family Name", "family_name"),
            ("Primary Email", "email"),
            ("Job Title", "job_title"),
            ("Manager Email", "manager_email"),
            ("Location", "location"),
            ("Phone Number", "phone"),
        ]):
            tk.Label(root, text=label_text).grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(root, width=40)
            entry.grid(row=i, column=1, columnspan=3, sticky="w")
            self.entries[var_name] = entry
        
        tk.Label(root, text="Department").grid(row=7, column=0, sticky="e", padx=5, pady=2)
        self.department_var = tk.StringVar()
        dept_menu = ttk.Combobox(root, textvariable=self.department_var, values=DEPARTMENTS, state="readonly", width=38)
        dept_menu.grid(row=7, column=1, columnspan=3, sticky="w")
        
        tk.Label(root, text="Password").grid(row=8, column=0, sticky="e", padx=5, pady=2)
        self.password_entry = tk.Entry(root, width=40, show="•")
        self.password_entry.grid(row=8, column=1, sticky="w")
        
        self.show_pw_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Show Password", variable=self.show_pw_var, command=self.toggle_password_visibility).grid(row=8, column=2, sticky="w")
        
        tk.Button(root, text="Generate Password", command=self.generate_password).grid(row=8, column=3, padx=5)
        
        self.change_pw_var = tk.BooleanVar()
        tk.Checkbutton(root, text="User must change password at next login", variable=self.change_pw_var).grid(row=9, column=1, columnspan=3, sticky="w", pady=2)
        
        # Text area for previewing groups before creation
        tk.Label(root, text="Groups to be added:").grid(row=10, column=0, sticky="nw", padx=5)
        self.groups_text = tk.Text(root, height=8, width=60, state="disabled")
        self.groups_text.grid(row=10, column=1, columnspan=3, pady=5)
        
        tk.Button(root, text="Preview Groups", command=self.preview_groups).grid(row=11, column=1, sticky="e", padx=2, pady=8)
        tk.Button(root, text="Clear Fields", command=self.clear_fields).grid(row=11, column=2, sticky="e", padx=2)
        self.create_button = tk.Button(root, text="Create User", command=self.create_user, bg="light grey")
        self.create_button.grid(row=11, column=3, sticky="e", padx=2)

    def toggle_password_visibility(self):
        if self.show_pw_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="•")

    def generate_password(self):
        pwd = generate_random_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, pwd)

    # Shows which groups the user will be added to before creation
    def preview_groups(self):
        data = self.collect_input()
        
        if not data["email"] or not data["given_name"] or not data["family_name"]:
            messagebox.showwarning("Missing Info", "At minimum, Given Name, Family Name, and Email are required.")
            return
        
        groups = determine_groups_to_add(data["department"], data["location"], data["job_title"])
        
        self.groups_text.config(state="normal")
        self.groups_text.delete("1.0", tk.END)
        self.groups_text.insert(tk.END, "\n".join(groups))
        self.groups_text.config(state="disabled")

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        
        self.department_var.set("")
        self.password_entry.delete(0, tk.END)
        self.change_pw_var.set(False)
        self.show_pw_var.set(False)
        self.password_entry.config(show="•")
        
        self.groups_text.config(state="normal")
        self.groups_text.delete("1.0", tk.END)
        self.groups_text.config(state="disabled")

    # Centralizes gathering of all form field values for consistency
    def collect_input(self):
        return {
            "given_name": self.entries["given_name"].get().strip(),
            "family_name": self.entries["family_name"].get().strip(),
            "email": self.entries["email"].get().strip(),
            "job_title": self.entries["job_title"].get().strip(),
            "department": self.department_var.get().strip(),
            "manager_email": self.entries["manager_email"].get().strip(),
            "location": self.entries["location"].get().strip(),
            "phone": self.entries["phone"].get().strip(),
            "password": self.password_entry.get().strip(),
            "change_password": "on" if self.change_pw_var.get() else "off",
        }

    # Creates the user in Google Workspace and adds them to groups
    def create_user(self):
        data = self.collect_input()

        # Validate required fields
        if not data["given_name"] or not data["family_name"] or not data["email"] or not data["department"] or not data["password"]:
            messagebox.showerror("Missing Fields", "Please fill in all required fields.")
            return
        
        # Set organizational unit path based on department
        org_unit_path = f"/{data['department']}"
        
        # Determine which groups the user should be added to
        groups = determine_groups_to_add(data["department"], data["location"], data["job_title"])
        
        # A message box that shows up to verify if info provided is correct
        confirm = messagebox.askyesno(
            "Confirm User Creation",
            f"Create user:\n\n"
            f"Name: {data['given_name']} {data['family_name']}\n"
            f"Email: {data['email']}\n"
            f"Department: {data['department']}\n"
            f"Org Unit: {org_unit_path}\n"
            f"Groups to be added:\n- " + "\n- ".join(groups)
        )
        
        if not confirm:
            return
        
        # Create the basic user account
        run_gam_command([
            "create", "user", data["email"],
            "firstname", data["given_name"],
            "lastname", data["family_name"],
            "password", data["password"],
            "changepassword", "true" if self.change_pw_var.get() else "false",
            "org", org_unit_path
        ])
        
        # This updates additional user properties in separate commands
        update_cmds = []
        if data["job_title"] or data["department"] or data["location"]:
            cmd = ["update", "user", data["email"], "organization"]
            if data["job_title"]: cmd += ["title", data["job_title"]]
            if data["department"]: cmd += ["department", data["department"]]
            if data["location"]: cmd += ["location", data["location"]]
            update_cmds.append(cmd)
        
        if data["phone"]:
            update_cmds.append(["update", "user", data["email"], "phones", "type", "work", "value", data["phone"]])
        
        if data["manager_email"]:
            update_cmds.append(["update", "user", data["email"], "manager", data["manager_email"]])
        
        for cmd in update_cmds:
            run_gam_command(cmd)
        
        # Add the user to all appropriate groups
        for group in groups:
            run_gam_command(["update", "group", group, "add", "member", data["email"]])
        
        messagebox.showinfo("Success", f"User {data['email']} created and added to groups.")

if __name__ == "__main__":
    root = tk.Tk()
    app = UserCreatorApp(root)
    root.mainloop()