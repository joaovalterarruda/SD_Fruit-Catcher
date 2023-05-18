from game_mech import GameMech
from server_skeleton import SkeletonServer


def main():
    gm = GameMech()
    gm.add_player("player", 5, 5)
    skeleton = SkeletonServer(gm)
    skeleton.run()


main()
