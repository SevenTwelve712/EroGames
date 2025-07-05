from configparser import ConfigParser
from TicTacToe import PROJECT_ROOT


class ResourcePack:
    def __init__(self, mode: str):
        conf_file = PROJECT_ROOT.joinpath('nsfw_rp', 'nsfw.conf') if mode == 'nsfw' \
            else PROJECT_ROOT.joinpath('sfw_rp', 'sfw.conf')

        config = ConfigParser()
        config.read(conf_file)

        pre = conf_file.parent
        self.tits_img = pre.joinpath(config['imgs']['cross'])
        self.ass_img = pre.joinpath(config['imgs']['null'])

        self.tits_name = config['names']['cross']
        self.ass_name = config['names']['null']
