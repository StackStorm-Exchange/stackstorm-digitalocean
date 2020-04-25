import digitalocean
import json
from st2common.runners.base_action import Action


class BaseAction(Action):

    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self._token = config['token']

    @staticmethod
    def digitalocean_obj_to_dict(obj):
        obj_dict = obj.__dict__
        # digitalocean.baseapi.BaseAPI has fields named _log and _session that don't like to be
        # serialized
        obj_dict.pop('_log', None)
        obj_dict.pop('_session', None)
        return obj_dict

    def do_action(self, cls, action, **kwargs):
        obj = getattr(digitalocean, cls)(token=self._token)
        digitalocean_results = getattr(obj, action)(**kwargs)
        # The results received from the digitalocean module are
        # custom python objects that StackStorm doesn't recognize.
        # The following code converts them into dicts & lists
        json_str = json.dumps(digitalocean_results, default=BaseAction.digitalocean_obj_to_dict)
        results = json.loads(json_str)
        return (True, results)
