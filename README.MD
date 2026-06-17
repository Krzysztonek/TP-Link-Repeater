TP-Link Range Extender Integration for Home Assistant



This custom component integrates TP-Link Wi-Fi Range Extenders (such as models RE650, RE450, and RE305) into Home Assistant. It operates entirely locally through the undocumented LuCI CGI web interface, utilizing the tplinkrouterc6u Python wrapper to handle the complex RSA/AES cryptographic login sequences required by modern TP-Link firmware.  

Features



Due to the hardware capabilities and proxy routing behaviors of TP-Link repeaters, this integration focuses on vital telemetry and radio statuses. It provides the following entities:



&#x20;   System Telemetry: CPU usage, Memory usage, and Device Uptime.  



&#x20;   Network Status: Total number of connected clients.  



&#x20;   Radio Interfaces (Binary Sensors): Active operational status of the 2.4GHz and 5GHz Wi-Fi transmitters.  



Note: The TP-Link web interface strictly allows only one active administrative session at a time. This integration is optimized to log in, fetch data via the DataUpdateCoordinator, and immediately log out to prevent locking you out of the web interface.  

Installation

Method 1: HACS (Recommended)



&#x20;   Open Home Assistant and navigate to HACS.



&#x20;   Click on the 3-dots menu in the top right corner and select Custom repositories.



&#x20;   Add the URL to your GitHub repository and select Integration as the category.  



&#x20;   Search for "TP-Link Range Extender" in HACS, click it, and select Download.  



&#x20;   Restart Home Assistant.  



Method 2: Manual



&#x20;   Download the latest release from this repository.



&#x20;   Copy the custom\_components/tplink\_repeater folder into the custom\_components directory of your Home Assistant configuration folder.  



&#x20;   Restart Home Assistant.  



Configuration



Configuration is managed entirely via the Home Assistant UI (Config Flow):



&#x20;   Go to Settings -> Devices \& Services.



&#x20;   Click the + Add Integration button in the bottom right corner.  



&#x20;   Search for TP-Link Range Extender.



&#x20;   Enter the required information:



&#x20;       Host: The local IP address of your repeater (e.g., 192.168.0.5).



&#x20;       Username: Typically admin (leave default even if your web interface only prompts for a password, as the API requires it to generate the cryptographic salt).  



&#x20;       Password: Your web interface administrator password.



&#x20;   Click Submit.



Troubleshooting



&#x20;   Cannot Connect (Timeout): Ensure your Home Assistant instance can route to the repeater's IP address. Repeater hardware with low memory/CPU limits may also occasionally drop TCP connections if under heavy load.



&#x20;   Invalid Authentication: Verify your password. If you recently flashed or modified the device, ensure the administrative password has not been reset to factory defaults.

