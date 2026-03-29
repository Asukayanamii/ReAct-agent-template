#!/usr/bin/env python3\
import yaml

class ConfigUtils:
    @classmethod
    def save_config(cls, config_file, config_data):
        with open(config_file, 'w',encoding='utf-8') as f:
            yaml.dump(config_data, f)

    @classmethod
    def load_config(cls, config_file):
        with open(config_file, 'r',encoding='utf-8') as f:
            config_data = yaml.load(f, Loader=yaml.FullLoader)
        return config_data