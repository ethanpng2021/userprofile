## What Should You Do If You Lost Your Administrator Password 

### Method 1: Use Another Administrator Account
If you have access to another account with administrative privileges:
1. Log in with the other administrative account.
2. Open **Command Prompt** as an administrator.
3. Reset the lost password by executing:
   ```shell
   net user Administrator newpassword
   ```
   Replace "newpassword" with the new password you want to set.

### Method 2: Utilize the "Offline NT Password & Registry Editor" (Third-Party Tool)
1. Download the Offline NT Password & Registry Editor from [its website](http://pogostick.net/~pnh/ntpasswd/).
2. Create a bootable USB drive or CD with the downloaded tool.
3. Boot your server from this USB drive or CD.
4. Follow the on-screen instructions provided by the tool to reset the administrator password.

### Method 3: Boot into Safe Mode with Command Prompt (If Applicable)
If you can boot into Safe Mode and the built-in administrator account (RID 500) is enabled:
1. Restart your server.
2. During boot, press the F8 key (or Shift + F8) before Windows starts loading to access Advanced Boot Options.
3. Select **Safe Mode with Command Prompt**.
4. Once the Command Prompt opens, execute the following command:
   ```shell
   net user Administrator newpassword
   ```
   Replace "newpassword" with the new password you want to set.
5. Restart the server and log in with the new password.

### Method 4: Use Windows Installation Media to Access Command Prompt
You can use the Windows Server 2019 installation media to access the Command Prompt:
1. Boot from the Windows Server 2019 installation DVD or USB.
2. On the first setup screen, press **Shift + F10** to open the Command Prompt.
3. Identify the drive letter of your Windows installation (commonly C: but may differ), and then execute the following commands:
   ```shell
   d:
   cd Windows\System32
   move utilman.exe utilman.exe.bak
   copy cmd.exe utilman.exe
   ```
   Replace `d:` with the correct drive letter if necessary.
4. Reboot the system normally. On the login screen, click the **Ease of Access** icon, which will open the Command Prompt.
5. In the Command Prompt, execute the following to reset the password:
   ```shell
   net user Administrator newpassword
   ```
   Replace "newpassword" with your desired password.
6. Restore the original files by rebooting into the installation media Command Prompt again and executing:
   ```shell
   d:
   cd Windows\System32
   move utilman.exe utilman.exe
   move utilman.exe.bak utilman.exe
   ```

### Method 5: Contact Microsoft Support
If none of the above methods work or are impractical for your situation, consider contacting Microsoft Support for assistance. They may provide additional methods or tools specific to your server setup.

Always remember to keep your passwords secure and consider using password management tools to avoid similar issues in the future.
