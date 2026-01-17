# **Pi-hole maintenance script**

A Pi-hole maintenance script that collects Teleporter backups and updates the Gravity database.

### **Requirements:**
* Python 3.7+ 


### **Setup:**
1. `git clone <repo-url>`
2. `cd pi-hole_backup_update`
3. `pip install -r requirements.txt `
4. Create an `.env` file inside the project folder with the following content:
```
PASSWORD="your_admin_password"
IP_LIST='["192.168.1.2", "192.168.1.3"]'
PATH_TO_BACKUP="path/to/backup"
```
* PASSWORD (_**mandatory**_) - string, non-empty.
* IP_LIST (_**mandatory**_) - list of strings in JSON format.
* PATH_TO_BACKUP (_optional_) - valid path, where backup files will be saved. 
If not present, defaults to "./backup"

**NOTE** - Be sure to secure .env file, as it contains plain-text password to your Pi-hole.  


### **Usage**
I use it with cron, running once per five days e.g.:

``0 0 */5 * * /home/user/Documents/pihole_update/.venv/bin/python main.py``

Logs will be stored inside project folder under name `backup_upgrade.log`
