# Adding Users on Windows 11

1. **Open Settings:**
   - Press `Win + I` to open the Settings app.

2. **Navigate to Accounts:**
   - In the Settings window, click on `Accounts` from the menu on the left side.

3. **Family & Other Users:**
   - In the Accounts section, click on `Family & other users`.

4. **Add a New User:**
   - Under the `Other users` section, click on `Add account`.

5. **Microsoft Account or Local Account:**
   - To add a local account instead of a Microsoft account:
     - Click on `I don't have this person's sign-in information`.
     - Then click on `Add a user without a Microsoft account`.

6. **Enter Account Information:**
   - Enter a username and password for the new user.
   - Fill out the security questions for password recovery.

7. **Finish Adding User:**
   - Click `Next` to create the new user account.

### Adding Users for Remote Access

1. **Open Control Panel:**
   - Press `Win + R`, type `Control Panel`, and press `Enter`.

2. **Navigate to System and Security:**
   - In the Control Panel, click on `System and Security`.

3. **Allow Remote Access:**
   - Under the `System` section, click on `Allow remote access`.

4. **System Properties:**
   - In the Remote tab of the System Properties window, ensure that `Allow Remote Assistance connections to this computer` is checked.
   - In the `Remote Desktop` section, select `Allow remote connections to this computer`.

5. **Add Users for Remote Access:**
   - Click on `Select Users` and then `Add`.

6. **Enter Usernames:**
   - Enter the username of the user you want to give remote access to (you can include both local and Microsoft accounts).

7. **Finish Setup:**
   - Click `OK` to close the dialog boxes and apply the changes.

### Note:

- **Remote Desktop Feature:** Remote Desktop is available on Windows 11 Pro, Enterprise, or Education editions. It is not available on Windows 11 Home.
- **Firewall and Network Settings:** Ensure that your firewall settings allow Remote Desktop connections and your network settings on both the client and the host machines permit remote access.

With these steps, the user should be added and able to access the computer remotely if the system configuration allows it.


# Adding Users on Windows Server 2019

1. **Open Server Manager:**
   - Click on the Start menu and select `Server Manager`.
   - If Server Manager does not open automatically, you can find it pinned to the taskbar or you can search for it in the Start menu.

2. **Navigate to Active Directory Users and Computers (if part of a domain):**
   - If your server is part of an Active Directory domain, go to `Tools` in the Server Manager dashboard and select `Active Directory Users and Computers`.
   - Right-click on the `Users` container (or an Organizational Unit where you want to add the user), and select `New > User`.

3. **Create a Local User (if not part of a domain):**
   - Open `Computer Management` from the Start menu or by running `compmgmt.msc`.
   - In the Computer Management console, navigate to `Local Users and Groups > Users`.
   - Right-click on `Users` and select `New User`.
   
4. **Enter User Details:**
   - Fill in the `Username`, `Full Name`, `Description` (optional), and `Password`. Ensure that `User must change password at next logon` is checked if you want the user to change it on the first login.
   - Click `Create` to add the new user.

### Granting Remote Access to Users

1. **Set Up Remote Desktop Services (if needed):**
   - Ensure that Remote Desktop Services is installed and configured on your server. You can add this role via Server Manager if it's not already installed.

2. **Enable Remote Desktop:**
   - Go to `Server Manager > Local Server`.
   - Click on `Remote Desktop` (usually marked as disabled by default), and configure it to `Allow remote connections`.

3. **Add Users to Remote Desktop Users Group:**
   - Open `Computer Management` as mentioned earlier.
   - Navigate to `Local Users and Groups > Groups`.
   - Double-click on the `Remote Desktop Users` group to open its properties.
   - Click on `Add` to add the users who need remote desktop access.
   - Enter the usernames, and click `OK`.

### Configuring Remote Desktop on Windows Server 2019

1. **Open System Properties:**
   - Right-click on `This PC` on the desktop or in File Explorer and select `Properties`.
   - Click on `Remote settings` in the left pane.

2. **Remote Tab Settings:**
   - In the Remote tab of the System Properties window, ensure that `Allow remote connections to this computer` is selected.
   - Click on `Select Users` and add the users or groups that need remote access.

3. **Firewall and Network Settings:**
   - Make sure that the firewall allows Remote Desktop connections. You can configure this in `Windows Defender Firewall`.
   - Open `Windows Defender Firewall with Advanced Security` from the Start menu.
   - Ensure that `Inbound Rules` for Remote Desktop (TCP-In) are enabled.

### Note:
- **Licensing:** For multiple users to connect simultaneously to a Windows Server using Remote Desktop, you may need Remote Desktop Services licenses (RDS CALs).
- **Security:** Ensure that users have strong passwords and that your network security is robust, especially if your server is accessible from the internet.

By following these steps, you can add users to your Windows Server 2019 and configure it so they can access it remotely. Ensure that you follow best practices for security and user management.
