from digitalocean_base_action_test_case import DigitalOceanBaseActionTestCase
from do import DigitalOceanManager
from lib.action import BaseAction
from st2common.runners.base_action import Action

import copy
import json
import mock


class TestLibAction(DigitalOceanBaseActionTestCase):
    __test__ = True
    action_cls = DigitalOceanManager
    maxDiff = None

    def test_init(self):
        action = self.get_action_instance(self.config_good)
        self.assertIsInstance(action, DigitalOceanManager)
        self.assertIsInstance(action, BaseAction)
        self.assertIsInstance(action, Action)
        self.assertEqual(action._token, self.config_good['token'])

    def test_init_empty_config_raises(self):
        with self.assertRaises(TypeError):
            self.get_action_instance(self.config_blank)

    def test_init_token_missing_raises(self):
        with self.assertRaises(KeyError):
            self.get_action_instance(self.config_incomplete)

    def test_digitalocean_obj_to_dict(self):
        expected = self.droplet_dict
        droplet = self.dict_to_droplet(expected)
        result = BaseAction.digitalocean_obj_to_dict(droplet)
        # The result may have an extra _session key, so make sure that result
        # is a subset of expected, see:
        # https://circleci.com/gh/StackStorm-Exchange/stackstorm-digitalocean/195
        # Unfortunately this method is not very transparent if the assertion
        # fails - there was a assertDictContainsSubset assertion, but it was
        # deprecated in Python 3.2 and presumably removed in Python 3.3
        # The hope here is that this assertion is properly relaxed (compared
        # to strict/simple equality), so it will not break very often.
        # See https://stackoverflow.com/a/9323769/6461688
        self.assertTrue(all(item in result.items() for item in expected.items()))

    def test_digitalocean_obj_to_dict__log_removed(self):
        expected = self.droplet_dict
        droplet_copy = copy.deepcopy(expected)
        droplet_copy['_log'] = "test log removed"
        droplet = self.dict_to_droplet(droplet_copy)
        result = BaseAction.digitalocean_obj_to_dict(droplet)
        self.assertTrue(all(item in result.items() for item in expected.items()))

    def test_digitalocean_obj_to_dict_json(self):
        expected = self.droplet_dict
        droplet = self.dict_to_droplet(expected)
        result = BaseAction.digitalocean_obj_to_dict(droplet)
        self.assertTrue(all(item in result.items() for item in expected.items()))

        json_str = json.dumps(droplet, default=BaseAction.digitalocean_obj_to_dict)
        json_result = json.loads(json_str)
        self.assertEqual(json_result, expected)

    @mock.patch('digitalocean.Droplet')
    def test_do_action(self, mock_droplet_cls):
        config = self.config_good
        action_instance = self.get_action_instance(config)

        cls = "Droplet"
        action = "get_droplet"
        fake_droplet = self.dict_to_droplet(self.droplet_dict)
        expected_kwargs_dict = {'arg1': 'value1',
                                'arg2': 2}

        mock_droplet_obj = mock.MagicMock()
        mock_droplet_obj.get_droplet.return_value = fake_droplet
        mock_droplet_cls.return_value = mock_droplet_obj

        result = action_instance.do_action(cls, action, **expected_kwargs_dict)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], self.droplet_dict)
        mock_droplet_cls.assert_called_with(token=config['token'])
        mock_droplet_obj.get_droplet.assert_called_with(**expected_kwargs_dict)

    @mock.patch('digitalocean.Droplet')
    def test_run(self, mock_droplet_cls):
        config = self.config_good
        action_instance = self.get_action_instance(config)

        cls = "Droplet"
        action = "get_droplet"
        fake_droplet = self.dict_to_droplet(self.droplet_dict)
        expected_action_kwargs = {'action_arg1': 'value1',
                                  'action_arg2': 2}
        run_kwargs = {'action': action,
                      'cls': cls}
        run_kwargs.update(expected_action_kwargs)

        mock_droplet_obj = mock.MagicMock()
        mock_droplet_obj.get_droplet.return_value = fake_droplet
        mock_droplet_cls.return_value = mock_droplet_obj

        result = action_instance.run(**run_kwargs)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], self.droplet_dict)
        mock_droplet_cls.assert_called_with(token=config['token'])
        mock_droplet_obj.get_droplet.assert_called_with(**expected_action_kwargs)

    def test_run_missing_cls(self):
        action_instance = self.get_action_instance(self.config_good)
        run_kwargs = {'action': 'get_droplet'}
        with self.assertRaises(KeyError):
            action_instance.run(**run_kwargs)

    def test_run_missing_action(self):
        action_instance = self.get_action_instance(self.config_good)
        run_kwargs = {'cls': 'Droplet'}
        with self.assertRaises(KeyError):
            action_instance.run(**run_kwargs)

    def test_run_no_kwargs(self):
        action_instance = self.get_action_instance(self.config_good)
        with self.assertRaises(KeyError):
            action_instance.run()
