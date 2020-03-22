import sys

ai_name = sys.argv[1]
#this generates a skeleton for an ai scheme
f=open("./axiom/ai_plugins/" + ai_name + ".py", "w")

f.write("from game import *\n")
f.write("\n")
f.write("from ai_plugins.dominion_ai import AI\n")
f.write("\n")
f.write("class "+ ai_name.title() + "(AI):\n")
f.write("\tdef __init__(self, _name):\n")
f.write("\t\tself.name = _name\n")
f.write("\n")
f.write("\t#def process_decision_params(self, _stip, _optional):\n")
f.write("\t\t# prepreocessing for decision stipuliation and optional flag\n")
f.write("\t\t# use this for common operations if necessary so you can write less code in your decision functions\n")
f.write("\t\t# see any of the pre-defined ai schemes for an example of this\n")
f.write("\n")
f.write("\t#def action_fn(self, _game, _player, _stip, _optional):\n")
f.write("\t\t# given a game state and a player with an oppurtunity to play an action, \n\t\t# return an action card from the player's hand \n")
f.write("\t\t# stipulation: returns cards that the player is allowed to play (if there is a restriction),\n\t\t# given the player's hand\n")
f.write("\n")
f.write("\t#def discard_fn(self, _game, _player, _stip, _optional):\n")
f.write("\t\t# given a game state and a player with an oppurtunity to dicard a card, \n\t\t# return a card in tha player's hand to discard\n")
f.write("\t\t# stipulation: cards that the player is allowed to discard (if there is a restriction), \n\t\t# given the player's hand\n")
f.write("\n")
f.write("\t#def buy_fn(self, _game, _player, _stip, _optional):\n")
f.write("\t\t# given a game state and a player with an oppurtunity to purchase a card, \n\t\t# return a card that is available in the shop and that the player can afford\n")
f.write("\t\t# stipulation: cards that the player is allowed to buy from the shop (if there is a restriction), \n\t\t# note that this is different from the restriction imposed by the player's hand value (i.e. coins)\n")
f.write("\n")
f.write("\t#def trash_fn(self, _game, _player, _stip, _optional):\n")
f.write("\t\t# given a game state and a player with an oppurtunity to trash a card, \n\t\t# return a card from the player's hand\n")
f.write("\t\t# stipulation: cards that the player is allowed to trash (if there is a restriction), \n\t\t# given the player's hand\n")
f.write("\n")
f.write("\t#def gain_fn(self, _game, _player, _stip, _optional):\n")
f.write("\t\t# given a game state and a player with an oppurtunity to gain a card, \n\t\t# return a card that is available in the shop\n")
f.write("\t\t# stipulation: cards that the player is allowed to gain from the shop (there almost always will be a restriction here)\n")
f.write("\n")
f.write("\t#def put_on_top_fn(self, _game, _player, _stip, _optional):\n")
f.write("\t\t# given a game state and a player with an oppurtunity to put a card on top of their deck, \n\t\t# return a card in the player's hand to put on top\n")
f.write("\t\t# stipulation: cards that the player is allowed to put on top (if there is a restriction), \n\t\t# given the player's hand\n")
f.write("\t\n")
f.close()