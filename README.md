## Create User in Google Wokrspace GUI Script - Quick Start

There are two versions of this script: one with **hardcoded groups** (Create_User_GWS-Hardcoded.py) and this **dynamic version** (Create_User_GWS-Dynamic.py). The hardcoded version was created to demonstrate how the group assignment logic works, while this dynamic version builds on that logic by fetching group data directly from Google Workspace to ensure accuracy and ease of maintenance.

This version of the script dynamically fetches the list of groups directly from Google Workspace using GAM, ensuring it always works with the most current group information. This dynamic approach is more convenient because it eliminates the need to manually update the script whenever groups change or new groups are added. In contrast, the earlier version used a hardcoded list of groups, which requires ongoing maintenance and risks becoming outdated. Dynamic fetching improves accuracy, reduces manual effort, and helps avoid errors caused by stale data.

### Create_User_GWS-Dynamic.py

#### Key Changes

- **Removed Hardcoded Dictionaries:**  
  The previous hardcoded group lists like `BASE_GROUPS`, `ROLE_GROUPS`, `BASE_LOCATION_GROUPS`, and `ROLE_LOCATION_GROUPS` are no longer used.

- **Added `fetch_all_groups` Method:**  
  This method runs the GAM command `gam print groups email` to retrieve all group emails from Google Workspace, handling errors gracefully.

- **Modified `determine_groups_to_add`:**  
  Now accepts an `all_groups` parameter and filters groups dynamically using string matching. The role keywords logic using regex remains unchanged.

- **Updated `UserCreatorApp`:**  
  - Fetches all groups once during initialization and stores them in `self.all_groups`.  
  - Passes `self.all_groups` to `determine_groups_to_add` in both `preview_groups` and `create_user` methods.

#### Summary:
- Groups are **not hardcoded anywhere** in the script.
- Instead, the script calls GAM (`gam print groups email`) and parses the output to build a list of group emails.
- This list (`self.all_groups`) is then used throughout the script to determine appropriate groups for the user.
- If GAM or the network is unavailable, it will show error/warning dialogs, and the groups list will be empty.

---

**Note:**  
For this script to work correctly, GAM must be installed, configured, and accessible from your system's PATH. Network connectivity is required to fetch group data from Google Workspace. If GAM is not available or network issues occur, the script will display appropriate error or warning messages, and group-related functionality will be limited.

Instructions to set up your environment with Python and GAM including OAuth authorization to be able to run the GUI script.

---

## Table of Contents

* [Prerequisites](#prerequisites)
* [Installing Python](#installing-python)

  * [Windows](#windows)
  * [Linux](#linux)
  * [Mac](#mac)
* [Installing GAM](#installing-gam)
* [GAM OAuth Authorization with Google Workspace](#gam-oauth-authorization-with-google-workspace)
* [Usage](#usage)
* [Support](#support)

---

## Prerequisites

* Google Workspace Admin account
* Internet connection for downloading tools and authorization

---

## Installing Python

Python is required to run GAM. Follow the instructions below to install Python on your operating system.

### Windows

1. Download the latest Python installer from the official site:
   [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
2. Run the installer.
3. **Important:** Check **Add Python to PATH** before installation.
4. Click **Install Now** and follow the prompts.
5. Verify installation by opening Command Prompt and running:

   ```bash
   python --version
   ```

### Linux

Most Linux distros come with Python 3 pre-installed. If not, install it via your package manager.

For Debian/Ubuntu:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

For Fedora:

```bash
sudo dnf install python3 python3-pip
```

Verify installation:

```bash
python3 --version
```

### Mac

1. macOS ships with Python 2.x by default; install Python 3.x via Homebrew.
2. Install Homebrew if not installed:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Python 3:

   ```bash
   brew install python
   ```
4. Verify installation:

   ```bash
   python3 --version
   ```

---

## Installing GAM

GAM is a command-line tool for managing Google Workspace domains.

1. Download the latest version of GAM from the official GitHub releases page:
   [https://github.com/jay0lee/GAM/releases](https://github.com/jay0lee/GAM/releases)
2. Choose the appropriate package for your OS (Windows `.exe`, Linux `.tar.xz`, or Mac `.pkg` / binary).
3. Follow the installation instructions for your OS:

   * **Windows:** Run the `.exe` installer and follow the prompts.
   * **Linux/Mac:** Extract the archive and run the install script. For example:

     ```bash
     tar -xvJf gam-linux-x64.tar.xz
     cd gam-linux-x64
     sudo ./install.sh
     ```
4. Verify installation by running:

   ```bash
   gam version
   ```

---

## GAM OAuth Authorization with Google Workspace

To allow GAM to manage your Google Workspace, you need to authorize it with OAuth 2.0.

### Step 1: Create a Google Cloud Project

1. Go to Google Cloud Console: [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. Create a new project or select an existing one.
3. Navigate to **APIs & Services > Credentials**.
4. Click **Create Credentials > OAuth client ID**.
5. Configure the consent screen if prompted.
6. Select **Desktop app** and create the client.
7. Download the JSON credentials file.

### Step 2: Enable APIs and Required OAuth Scopes

Enable the following APIs for your project:

* Admin SDK
* Gmail API (if applicable)
* Directory API

Also, ensure the following OAuth scopes are authorized in your Google Cloud project to allow GAM full functionality:

* [https://www.googleapis.com/auth/admin.directory.user](https://www.googleapis.com/auth/admin.directory.user)
* [https://www.googleapis.com/auth/admin.directory.group](https://www.googleapis.com/auth/admin.directory.group)
* [https://www.googleapis.com/auth/admin.directory.group.member](https://www.googleapis.com/auth/admin.directory.group.member)

Enable APIs here: [https://console.cloud.google.com/apis/library](https://console.cloud.google.com/apis/library)

### Step 3: Configure GAM

1. Place the downloaded JSON credentials file in your GAM config directory (usually `~/.gam`).
2. Run the OAuth authorization command:

   ```bash
   gam oauth create
   ```
3. Follow the prompts to authorize GAM. This usually involves opening a URL in your browser, logging into your Google Workspace Admin account, and granting permissions.

### Step 4: Verify Authorization

Test by running a simple command, e.g.:

```bash
gam info user admin@yourdomain.com
```

If the command returns user info, OAuth is set up successfully.

---

## Usage

After installation and authorization, you can begin using GAM to manage your Google Workspace environment. Refer to the official GAM documentation for commands and advanced configuration:
[https://github.com/jay0lee/GAM/wiki](https://github.com/jay0lee/GAM/wiki)

---

## Support

If you run into issues:

* Check the Issues page of this repository.
* Refer to the official GAM GitHub: [https://github.com/jay0lee/GAM](https://github.com/jay0lee/GAM)
* Google Workspace Admin Help: [https://support.google.com/a/](https://support.google.com/a/)
