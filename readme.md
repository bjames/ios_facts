Simply gathers information about an IOS device. Currently the following information is gathered:

1. Running image or image version
2. Boot directory (Ie. bootflash or flash)
3. Configuration Register
4. Running configuration
5. Number of SUPs
6. State of the secondary SUP (True if state is standby hot, false otherwise)
7. Number of connected interfaces
8. Number of authenticated clients (dot1x)
9. Number of directly connected routes
10. Number of external routes

This is meant to be used to validate devices either before or after an automated change. More features will be added as needed.

**get_facts(ssh_session)**

Function only requires a netmiko object and returns a dictionary