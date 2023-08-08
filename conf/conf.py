import configparser

config_file_path = "config/env.ini"


# 加载配置文件
def load_config():
    config = configparser.ConfigParser(default_section='lower')
    with open(config_file_path, 'r', encoding='utf-8') as f:
        config.read_file(f)
        f.close()
    return config