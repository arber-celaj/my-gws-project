## Create User in Google Wokrspace GUI Script - Quick Start

---

# This repository provides instructions to set up your environment with Python and GAM for managing Google Workspace domains, including OAuth authorization setup.

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
