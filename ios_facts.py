import re, netmiko, getpass


def get_confreg(ssh_session):

    ''' returns the configured bootvariable '''

    # Some IOS devices list the firmware revision using hex, so we need to find the config register line first
    regex_confreg_line = re.compile('Configuration register is 0x[a-fA-F\d]*')
    regex_confreg = re.compile('0x[a-fA-F\d]*')

    output = ssh_session.send_command('show version')

    confreg_line = regex_confreg_line.search(output).group()
    confreg = regex_confreg.search(confreg_line).group()

    return confreg


def get_redundancy_mode(ssh_session):

    ''' returns the redundancy mode on daul SUP devices '''

    output = ssh_session.send_command('show redundancy')

    if 'Stateful Switchover' in output:

        return True

    else:

        return False


def get_redundancy_status(ssh_session):

    ''' returns the redundancy status on dual SUP devices '''

    output = ssh_session.send_command('show redundancy')

    if 'STANDBY HOT' in output:

        return True

    elif 'STANDBY COLD' in output:

        return False

    else:

        raise AttributeError('redundancy mode is neither standby hot or standby cold')


def get_sups(ssh_session):

    ''' returns the number of SUPs installed '''

    regex_sups = re.compile('SUP')

    output = ssh_session.send_command('show module')

    return len(regex_sups.findall(output))


def get_directory(ssh_session):

    ''' gets the device's boot directory '''

    regex_flash = re.compile('[A-Za-z]*flash:/')

    output = ssh_session.send_command('dir | i :/')

    return regex_flash.search(output).group()


def get_install_mode(ssh_session):

    ''' returns true if the image is running in install mode, false otherwise '''

    if 'INSTALL' in ssh_session.send_command('show version | i INSTALL'):
        
        return True

    return False


def get_image_version(ssh_session):

    ''' returns the current running IOS image version '''

    re_ver = re.compile('[\d+\.]*\.[a-zA-Z\.\d]*')

    output = ssh_session.send_command('show version | i Cisco IOS')

    return re_ver.search(output).group()


def get_image(ssh_session):

    ''' returns the current running IOS image '''

    regex_image = re.compile('[A-Za-z\d\.-]*.bin')

    output = ssh_session.send_command('show version')

    return regex_image.search(output).group()


def get_config(ssh_session):

    ''' returns the running config '''

    return ssh_session.send_command_expect('sh run')


def get_connected_route_count(ssh_session):

    ''' returns the number of directly connected routes '''

    regex_route = re.compile('directly')

    output = ssh_session.send_command('show ip route')

    return len(regex_route.findall(output))


def get_external_route_count(ssh_session):

    ''' returns the size of the routing table '''

    regex_route = re.compile('via')

    output = ssh_session.send_command('show ip route')

    return len(regex_route.findall(output))


def get_auth_sessions_count(ssh_session):

    ''' returns the number of authentication sessions '''

    regex_auth = re.compile('Auth  ')

    output = ssh_session.send_command('show authentication sessions')

    return len(regex_auth.findall(output))


def get_connected_interface_count(ssh_session):

    ''' returns the number of connected interfaces '''

    regex_connected = re.compile('connected')

    output = ssh_session.send_command('show interface status')

    return len(regex_connected.findall(output))
    

def get_facts(ssh_session):

    ''' 
        gathers running IOS version, boot directory, number of SUPs, software install mode, etc 
        data is returned as a dictonary
    
    '''

    facts = {}


    try:

        try:
        
            facts['running_image'] = get_image(ssh_session)

        # if we cannot get the current running image, we get the version instead        
        except AttributeError:
            facts['running_image'] = get_image_version(ssh_session)

        facts['boot_directory'] = get_directory(ssh_session)
        facts['install_mode'] = get_install_mode(ssh_session)
        facts['confreg'] = get_confreg(ssh_session)
        facts['running_config'] = get_config(ssh_session)
        facts['number_sups'] = get_sups(ssh_session)
        if facts['number_sups'] >= 2:

            facts['sso'] = get_redundancy_mode(ssh_session)
            facts['standby_hot'] = get_redundancy_status(ssh_session)

        facts['connected_interfaces'] = get_connected_interface_count(ssh_session)
        facts['authenticated_clients'] = get_auth_sessions_count(ssh_session)
        facts['connected_routes'] = get_connected_route_count(ssh_session)
        facts['external_routes'] = get_external_route_count(ssh_session)

    except Exception:

        raise

    return facts


if __name__ == "__main__":

    ''' future use, allows get_facts to be run as a standalone file '''

    pass
