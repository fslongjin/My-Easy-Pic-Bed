#引入configparser包，它是用于读取配置文件的包
#配置文件的格式可以为[](其中包含的为section)
import configparser
import os


def get_path():
    current_path = os.path.abspath(__file__)
    print(os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep ), 'config.ini'))
    return os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep), 'config.ini')


#定义读取配置文件的函数，分别读取section中的配置参数

def get_config(config_file=get_path()):
    parser = configparser.ConfigParser()
    parser.read(config_file)
    #获取整型参数，按照key-value的形式保存
    _conf_ints = [(key, int(value)) for key, value in parser.items('ints')]

    #获取字符型参数，按照key-value的形式保存
    _conf_strings = [(key, str(value)) for key, value in parser.items('strings')]


    #返回一个字典对象，包含读取的参数
    return dict(_conf_ints + _conf_strings )

