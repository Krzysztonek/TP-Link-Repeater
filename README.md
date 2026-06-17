# TP-Link Range Extender Integration for Home Assistant

This custom component integrates TP-Link Wi-Fi Range Extenders (such as models RE650, RE450, and RE305) into Home Assistant. It operates entirely locally through the undocumented LuCI CGI web interface, utilizing the tplinkrouterc6u Python wrapper to handle the complex RSA/AES cryptographic login sequences required by modern TP-Link firmware.  
Features

Due to the hardware capabilities and proxy routing behaviors of TP-Link repeaters, this integration focuses on vital telemetry and radio statuses. It provides the following entities:

    System Telemetry: CPU usage, Memory usage, and Device Uptime.  
    Network Status: Total number of connected clients.  
    Radio Interfaces (Binary Sensors): Active operational status of the 2.4GHz and 5GHz Wi-Fi transmitters.  

Note: The TP-Link web interface strictly allows only one active administrative session at a time. This integration is optimized to log in, fetch data via the DataUpdateCoordinator, and immediately log out to prevent locking you out of the web interface.  
Installation
Method 1: HACS (Recommended)

    Open Home Assistant and navigate to HACS.
    Click on the 3-dots menu in the top right corner and select Custom repositories.
    Add the URL to your GitHub repository and select Integration as the category.  
    Search for "TP-Link Range Extender" in HACS, click it, and select Download.  
    Restart Home Assistant.  

Method 2: Manual

    Download the latest release from this repository.
    Copy the custom_components/tplink_repeater folder into the custom_components directory of your Home Assistant configuration folder.  
    Restart Home Assistant.  

Configuration

Configuration is managed entirely via the Home Assistant UI (Config Flow):

    Go to Settings -> Devices & Services.
    Click the + Add Integration button in the bottom right corner.  
    Search for TP-Link Range Extender.
    Enter the required information:
        Host: The local IP address of your repeater (e.g., 192.168.0.5).
        Username: Typically admin (leave default even if your web interface only prompts for a password, as the API requires it to generate the cryptographic salt).  
        Password: Your web interface administrator password.
    Click Submit.

Troubleshooting

    Cannot Connect (Timeout): Ensure your Home Assistant instance can route to the repeater's IP address. Repeater hardware with low memory/CPU limits may also occasionally drop TCP connections if under heavy load.
    Invalid Authentication: Verify your password. If you recently flashed or modified the device, ensure the administrative password has not been reset to factory defaults.
