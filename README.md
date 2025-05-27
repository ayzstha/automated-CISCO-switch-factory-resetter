# Cisco Switch Factory Reset Tool

This Python script uses the [Netmiko](https://github.com/ktbyers/netmiko) library to perform a **factory reset** on a Cisco IOS switch via SSH. It safely deletes the `vlan.dat` file, erases the startup configuration, and reloads the device.

## 🚀 Features

- ✅ SSH login with username/password
- 🔍 Scans all flash-like storage locations for `vlan.dat`
- 🗑 Deletes `vlan.dat` (removes VLAN database)
- 💾 Erases startup configuration (`write erase`)
- 🔄 Reloads the switch and closes the session safely
- 🔐 Prompts for confirmation to prevent accidental resets

## 📋 Prerequisites

- Python 3.7+
- Install dependencies:

  ```bash
  pip install netmiko
  ```

## 🧠 How It Works

1. Connects to the Cisco switch using SSH credentials.
2. Searches all storage locations (like `flash:`, `bootflash:`, `nvram:`) for `vlan.dat`.
3. Deletes `vlan.dat` if found.
4. Erases the startup configuration.
5. Reloads the switch.
6. Disconnects the session before timeout issues occur.

## 🛠 Usage

```bash
python reset_switch.py
```

You'll be prompted to enter:
- Switch IP address
- SSH username
- SSH password
- Confirmation before wiping and reloading

## ⚠️ Warning

This script will:
- Permanently delete configuration files
- Reboot the switch
- Interrupt network access temporarily

Only run this script on devices you intend to factory reset.

## 🧑‍💻 Author

**Aayush Shrestha**  
Network Engineer Intern & Software Developer

---

✅ Tested on Cisco IOS switches  
📡 Contributions and suggestions welcome!
