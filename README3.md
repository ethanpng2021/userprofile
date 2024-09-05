CrowdStrike is a popular cybersecurity software known for its endpoint protection capabilities. However, uninstalling it requires administrative access and sometimes specific tools from CrowdStrike, especially if your organization has used tamper protection.

### Steps to Uninstall CrowdStrike Falcon Sensor

#### 1. **Obtain the CrowdStrike Uninstaller**

CrowdStrike typically provides uninstallers directly through their support channels, as it’s a business-focused solution. You might need to contact your IT department or CrowdStrike support for the official uninstaller.

#### Option 1: Standard Uninstallation via Control Panel

1. **Open the Control Panel:**
   - Press `Windows + R`, type `control`, and press Enter.

2. **Navigate to Programs and Features:**
   - Click on **"Uninstall a program"** under the Programs section.

3. **Locate CrowdStrike Falcon Sensor:**
   - Find `CrowdStrike Falcon Sensor` in the list of installed programs.

4. **Uninstall:**
   - Right-click on `CrowdStrike Falcon Sensor` and select **Uninstall**.
   - Follow the on-screen prompts to complete the uninstallation.

#### Option 2: Uninstallation via Command Line

If the above method doesn't work, you can try uninstalling CrowdStrike Falcon Sensor using the command line. Administrative privileges are required for this.

1. **Open Command Prompt as Administrator:**
   - Press the `Start` button, type `cmd`, right-click on `Command Prompt`, and select **Run as administrator**.

2. **Run Uninstall Command:**
   - Enter the following command:
     ```shell
     sc query csagent
     ```
   - If the service exists, stop it using:
     ```shell
     sc stop csagent
     ```
   - Then, use the MSI exec command for uninstallation:
     ```shell
     msiexec /x {Product Code}
     ```
     To find the `{Product Code}`, you may need to check the registry. Navigate to:
     ```shell
     HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall
     ```
   - Look for `CrowdStrike Falcon Sensor` and find the `Product Code`.

#### Option 3: Using CrowdStrike Uninstall Protection Tool

If your organization uses CrowdStrike’s tamper protection, you'll need to disable it first. This sometimes involves obtaining an "uninstall token" from your CrowdStrike console.

1. **Contact Your IT Department:**
   - Reach out to your IT department or CrowdStrike administrator.

2. **Obtain Uninstall Token:**
   - They can generate an uninstall token from the CrowdStrike console:
     - Go to `Hosts` > `Host Management`.
     - Find and select the specific host.
     - Click on `More actions` > `Generate uninstall token`.

3. **Uninstall Using the Token:**
   - Open an **Administrator Command Prompt**.
   - Run the following command with the appropriate token:
     ```shell
     C:\Program Files\CrowdStrike\CSFalconContainer.exe /uninstall /uninstall_token=<your_token_here>
     ```
     Replace `<your_token_here>` with the actual token provided.

### Note:
1. **Permissions:** Ensure you have administrative permissions to perform the uninstallation.
2. **Documentation:** Consult CrowdStrike’s official documentation or support for any specific details related to your deployment.

### Contacting CrowdStrike Support
If you're facing issues, consider contacting CrowdStrike support:

1. **Visit the CrowdStrike Support Portal:** [CrowdStrike Support Portal](https://www.crowdstrike.com/support/)
2. **Login:** Use your CrowdStrike account credentials to log in.
3. **Submit a Ticket:** Follow the prompts to submit a support ticket for guidance on the uninstallation process.

By following these steps, you should be able to uninstall CrowdStrike Falcon Sensor from your Windows machine.
