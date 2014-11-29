import sys
from game import Game
from levelreader import LevelReader

def load_level (file_path) :
	reader = LevelReader ()
	game = reader.read (file_path)
	game.run ()

def main () :
	assert (len (sys.argv) == 2)
	load_level (sys.argv[1])

if __name__ == '__main__' :
	main ()