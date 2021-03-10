import yaml
from passlib.hash import sha512_crypt


class CloudInitGenerator(object):

    def __init__(self):
        self.finalstuff = []

    def addNewClass(self, o):
        if issubclass(o, BaseYamlObject):
            self.finalstuff.append(o)
        else:
            raise TypeError('Class must be a subclass.')

    def exportAsYaml(self):
        jankdict = {}
        for stuff in self.finalstuff:
            jankdict.update(stuff.getObject())
        return f'#cloud-config\n{yaml.safe_dump(jankdict)}'


class BaseYamlObject(object):
    def getObject(self):
        return vars(self)

    def getYaml(self):
        return yaml.safe_dump(self.getObject())


class Groups(BaseYamlObject):

    def __init__(self):
        self.groups = []

    def addGroup(self, groupname, groupmembers=None):
        if isinstance(groupname, str) and groupmembers is None:
            self.groups.append(groupname)
        elif isinstance(groupname, str) and isinstance(groupmembers, list):
            self.groups.append({groupname: groupmembers})
        else:
            raise TypeError('Group elements must be either a string or a dict in the '
                            'notation of {\'groupname\': ["list", "of", "users"]')


class Users(BaseYamlObject):

    def __init__(self, enableDefaultUser=True):
        self.users = []
        if enableDefaultUser:
            self.users.append('default')

    # PRO MODE:
    # Adds in the user without whatever validation
    def addUsersFromDict(self, userdict):
        if isinstance(userdict, dict):
            self.users.append(userdict)

    def addUser(self, name, gecos=None, primary_group=None, groups=None, selinux_user=None, expiredate=None,
                ssh_import_id=None, lock_passwd=None, passwd=None):
        newuser = {}
        newuser.update({'name': name})
        if isinstance(gecos, str):
            newuser.update({'gecos': gecos})
        else:
            newuser.update({'gecos': name})

        if isinstance(primary_group, str) and primary_group is not None:
            newuser.update({'primary_group': primary_group})

        if isinstance(groups, list):
            newuser.update({'groups': ', '.join(groups)})

        if isinstance(selinux_user, str):
            newuser.update({'selinux_user': selinux_user})

        if isinstance(passwd, str) and passwd.startswith(('$5$', '$6$')):
            # it is a hash so slap it into the dict
            newuser.update({'passwd': passwd})
        elif isinstance(passwd, str):
            newuser.update({'passwd': sha512_crypt.hash(passwd)})


class Packages(BaseYamlObject):

    def __init__(self, package_update=True, package_upgrade=True, package_reboot_if_required=True, packages=None):
        if packages is None:
            packages = []
        self.package_update = package_update
        self.package_upgrade = package_upgrade
        self.package_reboot_if_required = package_reboot_if_required
        self.packages = packages

    def enablePackageUpdate(self):
        self.package_update = True

    def enablePackageUpgrade(self):
        self.package_upgrade = True

    def disablePackageUpdate(self):
        self.package_update = False

    def disablePackageUpgrade(self):
        self.package_upgrade = False

    def enableRebootRequired(self):
        self.package_reboot_if_required = True

    def disableRebootRequired(self):
        self.package_reboot_if_required = False

    def addPackage(self, package):
        if isinstance(package, str):
            self.packages.append(package)
        elif isinstance(package, list):
            for f in package:
                if isinstance(f, str):
                    # What am I doing?
                    self.addPackage(f)

    def removePackage(self, package):
        if isinstance(package, str):
            self.packages.remove(package)
        elif isinstance(package, list):
            for f in package:
                if isinstance(f, str):
                    # What am I ACTUALLY doing?
                    self.removePackage(f)

    def dropPackages(self):
        self.packages = []
