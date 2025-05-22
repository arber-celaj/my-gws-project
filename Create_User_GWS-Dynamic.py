import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import subprocess
import re

# List of departments available in our organization
DEPARTMENTS = ["Core Business", "Engineering Support", "Finance", "HR", "Legal", "Management", "Marketing", "Operations Domain", "Organizations Super Admins", "Sales"]

# Mapping of full department names to simplified keys used in group names
DEPARTMENT_KEYS = {
    "core business": "core-business",
    "engineering support": "engineering",
    "finance": "finance",
    "hr": "hr",
    "legal": "legal",
    "management": "management",
    "marketing": "marketing",
    "operations domain": "operations",
    "organizations super admins": "super-admins",
    "sales": "sales"
}

def normalize_text(text):
    return text.lower().strip()

def generate_random_password(length=None):
    if length is None:
        length = random.randint(10, 12)
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Determines which groups a user should be added to based on department, location, and job title
def determine_groups_to_add(department, location, job_title, all_groups):
    groups_to_add = set()
    dept_clean = normalize_text(department or "")
    location_clean = normalize_text(location or "")
    job_title_clean = normalize_text(job_title or "")
    
    # Get the simplified department key for group matching
    dept_key = DEPARTMENT_KEYS.get(dept_clean, dept_clean)
    
    # Add department base groups: groups containing the department key, excluding role-specific groups
    for group in all_groups:
        if dept_key and dept_key in group.lower():
            if not any(keyword in group.lower() for keyword in ["manager", "lead", "director"]):
                groups_to_add.add(group)
    
    # Add role-specific department groups based on exact keyword match
    role_keywords = ["manager", "lead", "director"]
    for keyword in role_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', job_title_clean):
            # Look for groups like <dept_key>-<role>s or <dept_key>-<role>ship
            expected_groups = [
                f"{dept_key}-{keyword}s@deytech.se",
                f"{dept_key}-{keyword}ship@deytech.se"
            ]
            for expected_group in expected_groups:
                if expected_group in all_groups:
                    groups_to_add.add(expected_group)
    
    # Add base location groups: groups containing the location name, excluding management groups
    for group in all_groups:
        if location_clean and location_clean in group.lower():
            if "management" not in group.lower():
                groups_to_add.add(group)
    
    # Add role-specific location groups: look for <location>-management group
    if location_clean and any(re.search(r'\b' + re.escape(keyword) + r'\b', job_title_clean) for keyword in role_keywords):
        management_group = f"{location_clean}-management@deytech.se"
        if management_group in all_groups:
            groups_to_add.add(management_group)
    
    # Add default groups: groups containing "all-company" or "announcements"
    for group in all_groups:
        if any(default in group.lower() for default in ["all-company", "announcements"]):
            groups_to_add.add(group)
    
    return sorted(groups_to_add)

# Executes Google Admin SDK commands through GAM
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
        self.root.geometry("640x460")
        self.root.resizable(False, False)
        
        # Fetch all groups dynamically at startup
        self.all_groups = self.fetch_all_groups()
        
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
            tk.Label(self.root, text=label_text).grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(self.root, width=40)
            entry.grid(row=i, column=1, columnspan=3, sticky="w")
            self.entries[var_name] = entry
        
        tk.Label(self.root, text="Department").grid(row=7, column=0, sticky="e", padx=5, pady=2)
        self.department_var = tk.StringVar()
        dept_menu = ttk.Combobox(self.root, textvariable=self.department_var, values=DEPARTMENTS, state="readonly", width=38)
        dept_menu.grid(row=7, column=1, columnspan=3, sticky="w")
        
        tk.Label(self.root, text="Password").grid(row=8, column=0, sticky="e", padx=5, pady=2)
        self.password_entry = tk.Entry(self.root, width=40, show="•")
        self.password_entry.grid(row=8, column=1, sticky="w")
        
        self.show_pw_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Show Password", variable=self.show_pw_var, command=self.toggle_password_visibility).grid(row=8, column=2, sticky="w")
        
        tk.Button(self.root, text="Generate Password", command=self.generate_password).grid(row=8, column=3, padx=5)
        
        self.change_pw_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="User must change password at next login", variable=self.change_pw_var).grid(row=9, column=1, columnspan=3, sticky="w", pady=2)
        
        # Text area for previewing groups before creation
        tk.Label(self.root, text="Groups to be added:").grid(row=10, column=0, sticky="nw", padx=5)
        self.groups_text = tk.Text(self.root, height=8, width=60, state="disabled")
        self.groups_text.grid(row=10, column=1, columnspan=3, pady=5)
        
        tk.Button(self.root, text="Preview Groups", command=self.preview_groups).grid(row=11, column=1, sticky="e", padx=2, pady=8)
        tk.Button(self.root, text="Clear Fields", command=self.clear_fields).grid(row=11, column=2, sticky="e", padx=2)
        self.create_button = tk.Button(self.root, text="Create User", command=self.create_user, bg="light grey")
        self.create_button.grid(row=11, column=3, sticky="e", padx=2)

    def fetch_all_groups(self):
        """Fetch all group emails from Google Workspace using GAM."""
        command = ['gam', 'print', 'groups', 'email']
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                groups = stdout.strip().split('\n')
                # Filter out empty lines and the header (if any)
                groups = [group.strip() for group in groups if group.strip() and group.strip() != "email"]
                if not groups:
                    messagebox.showwarning("Warning", "No groups fetched from Google Workspace.")
                return groups
            else:
                messagebox.showerror("Error", f"Failed to fetch groups: {stderr}")
                return []
        except Exception as e:
            messagebox.showerror("Exception", f"Exception while fetching groups: {e}")
            return []

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
        
        groups = determine_groups_to_add(data["department"], data["location"], data["job_title"], self.all_groups)
        
        self.groups_text.config(state="normal")
        self.groups_text.delete("1.0", tk.END)
        self.groups_text.insert(tk.END, "\n".join(groups) if groups else "No groups found.")
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
        groups = determine_groups_to_add(data["department"], data["location"], data["job_title"], self.all_groups)
        
        # A message box that shows up to verify if info provided is correct
        confirm = messagebox.askyesno(
            "Confirm User Creation",
            f"Create user:\n\n"
            f"Name: {data['given_name']} {data['family_name']}\n"
            f"Email: {data['email']}\n"
            f"Department: {data['department']}\n"
            f"Org Unit: {org_unit_path}\n"
            f"Groups to be added:\n- " + ("\n- ".join(groups) if groups else "None")
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