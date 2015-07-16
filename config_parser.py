__author__ = 'tomtomssi'
import configparser


class ParseConfig:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('resources/config.ini')
        self.section = config['Credentials']

    def get_username(self):
        return self.section['Username']

    def get_password(self):
        return self.section['Password']

    def get_database(self):
        return self.section['Database']

    def get_host(self):
        return self.section['Host']

