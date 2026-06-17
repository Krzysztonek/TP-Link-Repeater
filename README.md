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
indicates that the integration script was unable to establish a proper connection with the repeater's administrative panel within the designated time, or the request was actively dropped by the device. Here are the most common causes for this error and how to resolve them:

    Active Session in a Browser or App (Most Common Cause):
    For security reasons, the TP-Link web interface strictly supports only one logged-in user at a time. If you have the router's panel open in a web browser or the TP-Link Tether app running on your smartphone while attempting to set up the integration in Home Assistant, the extender will immediately reject the new connection.

    Solution: Manually log out of the panel in your browser, completely close the Tether app, and try adding the integration again.

    Web Encrypted Password Requirement:
    Depending on your firmware version (especially after recent updates), the device may not accept your password in plain text and requires it to be encrypted by the web interface first.

    Solution: Go to the repeater's login page in your web browser. Type your password into the password field (but do not click log in). Click somewhere else on the page so the password field is no longer selected. Open your browser's Developer Tools (usually by pressing F12 and going to the "Console" tab). Type the command document.getElementById("login-password").value; and press Enter. Copy the long string of characters it returns and paste that into the password field in Home Assistant.

    Forced HTTPS Connection:
    If you have enabled "Local Management via HTTPS" in the advanced administration settings of your extender, attempting to connect using standard HTTP will result in a timeout or connection drop.

    Solution: In the Home Assistant configuration window, try forcing the secure protocol by typing it directly into the host field (e.g., https://192.168.0.5).

    Incorrect Username:
    While the vast majority of TP-Link devices use admin as the default username, some specific models and firmware versions use user instead. Double-check which username applies to your specific device.

    Dynamic IP Address:
    Make sure your range extender has a Static IP or DHCP Reservation assigned on your main home router. If the repeater restarted recently, it might have been assigned a completely new IP address by the DHCP server, making the old address unreachable.
