import yaml

class HParam:
    def __init__(self, hparam_yaml):
        with open(hparam_yaml) as f:
            hparams = yaml.load(f, Loader=yaml.FullLoader)
        for key, value in hparams.items():
            setattr(self, key, value)

hp = None

def set_hparam_yaml(yaml_path):
    global hp
    hp = HParam(yaml_path)
