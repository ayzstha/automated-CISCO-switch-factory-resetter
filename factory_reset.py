from netmiko import ConnectHandler
import getpass
import re

def find_and_delete_vlan(conn, switch_ip):
    print(f"Searching for vlan.dat on {switch_ip}...")

    # Step 1: Get possible storage locations
    base_output = conn.send_command("dir")
    
    # Regex to extract flash-like locations (e.g., flash:, bootflash:, nvram:)
    location_pattern = re.compile(r'\b(?:[\w\-]*flash[\w\-]*|nvram[\w\-]*):', re.IGNORECASE)
    flash_locations = list(set(location_pattern.findall(base_output)))

    if not flash_locations:
        print("No flash locations found.")
        return False

    # Step 2: Look for vlan.dat in each location
    vlan_pattern = re.compile(r'(\S*?vlan\.dat)', re.IGNORECASE)

    for location in flash_locations:
        output = conn.send_command(f'dir {location}')
        match = vlan_pattern.search(output)
        if match:
            full_path = match.group(1)
            print(f"Found vlan.dat at {full_path}")
            delete_cmds = [
                f'delete {full_path}',
                '\n',  # confirm filename
                '\n'   # confirm deletion
            ]
            for cmd in delete_cmds:
                conn.send_command_timing(cmd)
            print(f"Deleted vlan.dat from {full_path}")
            return True

    print(f"vlan.dat not found on {switch_ip}")
    return False

def reset_switch(device_info, username, password, switch_ip):
    device_info['username'] = username
    device_info['password'] = password
    device_info['secret'] = password

    try:
        print(f"\nConnecting to {switch_ip}...")
        conn = ConnectHandler(**device_info)
        conn.enable()

        find_and_delete_vlan(conn, switch_ip)

        print(f"Erasing startup-config on {switch_ip}...")
        conn.send_command_timing('write erase')
        conn.send_command_timing('\n')  # confirm

        print(f"Reloading {switch_ip}...")
        output = conn.send_command_timing('reload')
        if 'Save' in output:
            conn.send_command_timing('no')
        if 'confirm' in output.lower():
            conn.send_command_timing('\n')

        print(f"\nReload command sent. Closing SSH session as switch will reboot.")
        conn.disconnect()

    except Exception as e:
        print(f"Error resetting {switch_ip}: {e}")

def main():
    switch_ip = input("Enter the IP address of the switch to factory reset: ")
    username = input("Enter your SSH username: ")
    password = getpass.getpass("Enter your SSH password: ")

    print(f"\nWARNING: This will erase config and reload the switch at {switch_ip}.")
    confirm = input("Type 'Y' to confirm and continue: ")

    if confirm == 'Y':
        device_info = {
            'device_type': 'cisco_ios',
            'host': switch_ip
        }
        reset_switch(device_info, username, password, switch_ip)
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    main()
