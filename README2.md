# Recovery of Administrator PWD

### Method 1: Using Another Administrator Account

1. **Login with another administrator account**.
2. **Open Command Prompt with Administrative Privileges**:
   - Press `Win + X` and select "Command Prompt (Admin)".
3. **Reset the Password**:
   - Type the following command and press Enter:
     ```bash
     net user Administrator NewPassword
     ```
   - Replace `NewPassword` with your desired new password.

### Method 2: Using Safe Mode

1. **Restart the Server**.
2. **Boot into Advanced Boot Options**:
   - Press `F8` repeatedly while the server restarts to get the Advanced Boot Options menu.
3. **Select Safe Mode with Command Prompt**:
   - Use the arrow keys to select "Safe Mode with Command Prompt" and press Enter.
4. **Reset the Password** in Command Prompt:
   - Once you're in Safe Mode, a Command Prompt window should open. Type the following command and press Enter:
     ```bash
     net user Administrator NewPassword
     ```
   - Replace `NewPassword` with your desired new password.

### Method 3: Using the Installation Media (if you are locked out completely)

1. **Insert the Windows Server installation media (DVD/USB)** and restart the server.
2. **Boot from the installation media**:
   - You may need to press a key (such as `F2`, `F12`, `Esc`, or `Del`) to access the boot menu and select the installation media.
3. **Select "Repair your computer"**:
   - On the initial setup screen, click "Next," then choose "Repair your computer" in the lower-left corner.
4. **Open Command Prompt**:
   - Navigate to `Troubleshoot > Advanced options > Command Prompt`.
5. **Replace the Utilman.exe**:
   - Type the following commands to back up `Utilman.exe` and replace it with `cmd.exe`:
     ```bash
     move c:\windows\system32\utilman.exe c:\windows\system32\utilman.exe.bak
     copy c:\windows\system32\cmd.exe c:\windows\system32\utilman.exe
     ```
   - Replace `c:` with the appropriate drive letter if necessary.
6. **Reboot the Server**:
   - Close the Command Prompt and restart the server.
7. **Reset the Password**:
   - On the login screen, click the "Ease of Access" button (which should now open Command Prompt).
   - Type the following command and press Enter:
     ```bash
     net user Administrator NewPassword
     ```
   - Replace `NewPassword` with your desired new password.
8. **Restore the Original Utilman.exe**:
   - After logging in, replace the modified `utilman.exe` with the original file:
     ```bash
     copy c:\windows\system32\utilman.exe.bak c:\windows\system32\utilman.exe
     ```

### Method 4: Using a Third-Party Tool
There are several third-party tools available that can reset Windows passwords, like `ophcrack`, `PCUnlocker`, and others. Use them cautiously and ensure you have the proper legal authorization.

1. **Download and Create a Bootable USB/DVD** with the selected tool.
2. **Boot from the USB/DVD**:
   - Restart the server and boot from the third-party tool's USB/DVD.
3. **Follow the Tool's Instructions** to reset the administrator password.

Regardless of the method you choose, ensure you have proper authorization and all necessary precautions are in place to prevent data loss or security issues.
