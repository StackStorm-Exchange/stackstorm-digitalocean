import digitalocean
import json
from st2actions.runners.pythonrunner import Action


def digitalocean_obj_to_dict(obj):
    obj_dict = obj.__dict__
    # digitalocean.baseapi.BaseAPI has a field named _log that doesn't like to be serialized
    if "_log" in obj_dict:
        del obj_dict['_log']
    return obj_dict

class BaseAction(Action):

    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self._token = config['token']

    def do_action(self, cls, action, **kwargs):
        obj = getattr(digitalocean, cls)(token=self._token)
        digitalocean_results = getattr(obj, action)(**kwargs)
        # The results received from the digitalocean module are
        # custom python objects that StackStorm doesn't recognize.
        # The following code converts them into dicts & lists
        json_str = json.dumps(digitalocean_results, default=digitalocean_obj_to_dict)
        results = json.loads(json_str)
        return (True, results)
