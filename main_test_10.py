import pygame
import game_mech
import game_client

# This example has the following files:
# -- game2: main cycle in client side.
# -- player10: the player objects
# -- wall10: the wall objects
# -- game_mech_3: main file in server side.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pygame.init()
    # Create game mechanics with walls and other stuff
    gmech = game_mech_3.GameMech(30, 30)
    gmech.create_world()

    #gmech.add_obstacle('wall',20,20)
    #gmech.add_obstacle('wall',20,21)
    #gmech.add_obstacle('wall',20,22)
    #gmech.add_obstacle('wall',21,22)
    #gmech.add_obstacle('wall',21,20)
    #gmech.add_obstacle('wall',19,20)
    #gmech.add_obstacle('wall',22,22)
    #gmech.add_obstacle('wall',21,22)


    #gmech.add_obstacle('wall',17,20)
    #gmech.add_obstacle('wall',17,21)
    #gmech.add_obstacle('wall',17,22)
    #gmech.add_obstacle('wall',18,22)
    #gmech.add_obstacle('wall',19,22)


# Add a player (myself)
    nr = gmech.add_player('jose',28,2)
    nr = gmech.add_player('joao',10,10)

    # Start the visual part and the rest...
    gm = game2.Game(gmech,30)

    gm.run()

