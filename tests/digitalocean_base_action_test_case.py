from st2tests.base import BaseActionTestCase

import copy
from digitalocean import Droplet
import yaml


class DigitalOceanBaseActionTestCase(BaseActionTestCase):
    __test__ = False

    def setUp(self):
        super(DigitalOceanBaseActionTestCase, self).setUp()

        self._config_good = self.load_yaml('config_good.yaml')
        self._config_blank = self.load_yaml('config_blank.yaml')
        self._config_incomplete = self.load_yaml('config_incomplete.yaml')
        self._droplet_dict = self.load_yaml('droplet.yaml')

    def load_yaml(self, filename):
        return yaml.safe_load(self.get_fixture_content(filename))

    def dict_to_droplet(self, droplet_dict):
        droplet = Droplet()
        droplet_dict_copy = copy.deepcopy(droplet_dict)
        for key, value in droplet_dict_copy.items():
            setattr(droplet, key, value)
        return droplet

    @property
    def config_good(self):
        return self._config_good

    @property
    def config_blank(self):
        return self._config_blank

    @property
    def config_incomplete(self):
        return self._config_incomplete

    @property
    def droplet_dict(self):
        return self._droplet_dict
