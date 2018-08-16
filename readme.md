**Usage**
1. Add the submodule using 'git submodule add git@github.com:BJAMES4/ios_facts.git'
2. Import the submodule into your python projects as follows: 'from ios_facts.ios_facts import get_facts'
3. When ready, commit your changes and include the submodule: "git commit -am 'added ios_facts submodule'"
4. Push the changes 'git push origin master'
5. Git will automatically update the submodules when you 'git fetch'/'git merge origin/master' or you can manually update only the submodule with 'git submodule update --remote'

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

Function only requires a netmiko object and returns a dictionary. Many of the other functions provided by the module may be useful.