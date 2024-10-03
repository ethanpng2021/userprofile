### Backup the hosts complete Registry 
Start (Windows button) + R ---> Run ---> regedit
Right click 'Computer' and then click 'Export'. Save the registry (e.g. backup.reg).

### Disable csagent service
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CSAgent
set START to 4

### Disable Falcon Service
HKLM:\SYSTEM\CurrentControlSet\Services\CSFalconService
set START to 4

### Delete Folder
HKLM:\SYSTEM\CurrentControlSet\Services\CSFalconService

### Delete Folder
HKLM:\SYSTEM\CrowdStrike

### Delete Folder
HKLM:\SYSTEM\CurrentControlSet\Services\CSAgent\Sim

### Delete Folder
HKLM:\SYSTEM\CurrentControlSet\Services\CSAgent

### Reboot Server

### Uninstall from elevated command prompt with Uninstall Tool.

### Double-check inside "Add and Remove Programs".

### Reboot server again. Done.
