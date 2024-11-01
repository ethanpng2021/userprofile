To install MySQL on Ubuntu Server 22.04 and configure it, follow these steps:

### Step 1: Update Your System

First, make sure your package list and installed packages are up to date.

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install MySQL Server

You can install MySQL Server using the following command:

```bash
sudo apt install mysql-server -y
```

After installing, check whether it is running:
```bash
sudo systemctl status mysql
```

Useful commands:
```bash
sudo systemctl start mysql
sudo systemctl enable mysql (rarely used: allows autolaunching of mysql when you reboot the VPS)
sudo systemctl stop mysql
sudo systemctl restart mysql
sudo systemctl disable mysql (rarely used: stops autolaunching of mysql when you reboot the VPS)
```

### Step 3: Secure MySQL Installation

Once MySQL is installed, it’s a good practice to run the security script that comes with it. This will help secure your installation:

```bash
sudo mysql_secure_installation
```

You will be prompted for several configuration options. You can generally answer "Y" (yes) to most of them, especially to **set a root password**, **remove anonymous users**, **disallow root login remotely**, and **remove the test database**.

### Step 4: Allow MySQL through UFW

Next, you will need to open port 3306 for MySQL in the UFW firewall. Run these commands:

```bash
sudo ufw allow 3306/tcp
sudo ufw reload
```

Allow Remote Connections

To allow remote connections, edit the MySQL configuration file:

```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

Find this line

```ini
bind-address = 127.0.0.1
```

Change it to

```ini
bind-address = 0.0.0.0
```

Save the file (Ctrl-X, Yes, and then Enter), then restart MySQL:

```bash
sudo systemctl restart mysql
```

### Step 5: Log into MySQL as Root

Use the following command to log in to MySQL as root:

```bash
sudo mysql -u root -p
```

You will be prompted to enter the root password you set earlier.

Shortcut to log in as root:

```bash
sudo mysql
```

### Step 6: Create a New User and Grant Privileges

On Ubuntu 22.04, the root user **might be** configured to use auth_socket for authentication. To change this to password-based authentication:

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'YourStrongRootPassword';
FLUSH PRIVILEGES;
```

Otherwise just start with the following steps:

CREATE A LOCAL USER (for apps on the same server as the MySQL db)

To create a new user and give that user privileges on all databases, run the following SQL commands within the MySQL CLI.
Replace `newuser` with the username you want to create, and replace `password` with the desired password for that user:

```sql
CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'newuser'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

CREATE A REMOTE USER (for other servers to access your MySQL db)

If you want the new user to be able to connect from any host, you can replace `'localhost'` with `'%'`:

```sql
CREATE USER 'newuser'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'newuser'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

#### Nota Bene

In the SQL statement `GRANT ALL PRIVILEGES ON *.* TO 'newuser'@'%' WITH GRANT OPTION;`, the `*.*` indicates that the user is being granted privileges across all databases and all tables.

Breaking it down:

- The first `*` (before the dot) is a wildcard representing all databases accessible by the MySQL server. It means the privileges apply to any database.
- The second `*` (after the dot) is a wildcard for all tables within the databases. It means the privileges apply to any table within any database.

Therefore, `*.*` collectively specifies all tables across all databases on the MySQL server.

#### Implications of This Grant

- **Full Access**: The user `'newuser'` will have the specified privileges on every database and every table.
- **Admin-Level Permission**: Granting `ALL PRIVILEGES` provides comprehensive control, including the ability to SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, etc., along with database administration operations.
- **WITH GRANT OPTION**: This addition allows the user to grant the same privileges to other users, effectively making `'newuser'` a superuser or admin.

It is crucial to exercise caution when using such broad privileges to prevent accidental or intentional misuse of database resources. It is usually advisable to grant more specific permissions tailored to the user's needs.

### Step 7: Importing `.sql` Files

a. On the source db server, export each database into a *.sql file by using **mysqldump** (see Annex).\
b. Use WinSCP to copy out the sql files into your PC.\
c. Use WinSCP again to copy the sql files into the destination server (usually /home/user/). \
d. To import the `.sql` files into the destination MySQL, use the following command from your terminal:

```bash
mysql -u newuser -p database_name < /home/user/file.sql
mysql -u newuser -p database_name < /home/user/file_five_minutes.sql
```

Replace `newuser` with your MySQL username, `database_name` with the target database you want to import to, and `/home/user/file.sql` with the path to your `.sql` file.

### Step 8: Verify Everything is Set Up Correctly

You can log in as the new user to ensure the configuration works:

```bash
mysql -u newuser -p
```

After entering the password, you should be able to run commands and see that the user has access to the required databases.

---

This process should get MySQL installed and configured on your Ubuntu Server 22.04 setup, allowing you to manage your databases effectively. If you encounter issues, check for error messages during each step to diagnose the problem.

## Annex

Normal execution
```bash
mysqldump -u username -p database_name > /path/to/backup.sql
```

Pull from remote server save into local PC
```bash
mysqldump -u username -h 203.xxx.xxx.xxx -p database_name > /path/to/backup.sql
```

All the databases
```bash
mysqldump -u username -p --all-databases > /path/to/backup.sql
```

Export db with specific tables
```bash
mysqldump -u username -p database_name table1 table2 > /path/to/backup.sql
```

Export as root (to be used during emergency when you have errors)
```bash
mysqldump -u root -p example_db > /backups/example_db.sql
```
