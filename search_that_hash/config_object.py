import toml
from appdirs import *


def read_config_file():
    return read_and_parse_config_file(find_appdirs_location())


def find_appdirs_location():
    # TODO make this OS independent the "/" makes it Windows specific
    # print(user_config_dir("HashSearch", "Bee-san") + "/config.toml")
    pass
    # TODO where does this function exist lol
    # return user_config_dir("HashSearch", "Bee-san") + "/config.toml"


def read_and_parse_config_file(file):
    config_to_parse = read_file(file)

    if config_to_parse == None:
        return config_to_parse
    else:
        try:
            return toml.loads(config_to_parse)
        except:
            return None


def read_file(file):
    try:
        with open(file, "r") as out:
            return out.read()
    except:
        return None
