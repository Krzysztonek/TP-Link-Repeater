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
    It's possible that the integration script was unable to communicate correctly with the extender's admin panel within the allotted time, or the request was rejected by the device.

Given the specific nature of TP-Link devices, here are the most common causes of this error and how to resolve them:

Active session in browser or app (Most common cause):
The web interface of TP-Link devices only supports one logged-in user at a time for security reasons. If you have the router dashboard open in a web browser or the TP-Link Tether app open on your smartphone while attempting to configure the integration in Home Assistant, the extender will immediately reject the Home Assistant connection.

Solution: Manually log out of the browser dashboard, close the Tether app, and try adding the integration again.

Web Encrypted Password Requirement:
Depending on the firmware version (especially after updates), the device may not accept a plaintext password.

Solution: Go to the extender's login page in your browser and enter your password in the login field (do not click "Login" yet). Then, click elsewhere on the page and press F12 to open the browser's developer console. Enter the command: document.getElementById("login-password").value; and press Enter. Copy the long string returned and use it as the password in the Home Assistant configuration window.

Forced HTTPS Connection:
If you have enabled "Local Management via HTTPS" in the extender's advanced administration settings, attempting to connect via the standard HTTP port will result in an error.

Solution: In the Home Assistant configuration window, try forcing the protocol in the IP address field by entering, for example, https://192.168.0.5.

Incorrect Username:
Although most TP-Link devices use the admin account, some specific firmware versions use the default username "user." Confirm which of these values ​​is correct for your device.

Different Device IP Address:
Make sure the extender has a static IP address (Static IP / DHCP Reservation) assigned on your main home router. If the device has just restarted, it may have received a new IP address from the DHCP server.
