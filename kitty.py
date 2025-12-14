from kitty_move import move_legs, pca
from time import sleep

move_legs('all', 150, 100)

sleep(1)

move_legs('all', 90, 90)

pca.deinit()
