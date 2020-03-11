import random
import re
import copy
import importlib
import inspect

from game import Card, Deck, Player, Shop, Game
from ai_plugins.dominion_ai import AI
from shop_presets import *
from deck_presets import *

def import_AI(ai_name):
    if ai_name == 'dominion_ai':
        print('please specify the name of your AI file in the CL args rather than just "dominion_ai"')
        exit()
    try:
        module = importlib.import_module('ai_plugins.{0}'.format(ai_name))
        for x in dir(module):
            obj = getattr(module, x)
            if inspect.isclass(obj) and issubclass(obj, AI) and obj is not AI:
                return obj
    except ImportError:
        print('failed to import AI module "' + ai_name + '". Make sure "'+ ai_name + '.py" is present in the "ai_plugins" directory and has no syntax errors')
        exit()

def start_game(num_players, player_types):
    game_players = []
    for x in range(num_players):
        ai_type = import_AI(player_types[x])
        if ai_type:
            game_players += [Player(default_deck(), 'player' + str(x), ai_type(player_types[x]))]
        # if player_types[x] == 'Miser': 
        #     game_players += [Player(default_deck(), 'player' + str(x), Miser('miser'))]
        # elif player_types[x] == 'Common_Sense':
        #     game_players += [Player(default_deck(), 'player' + str(x), Common_Sense('common-sense'))]
        # else:
        #     game_players += [Player(default_deck(), 'player' + str(x), AI('random'))]
    game_shop = Shop(default_shop)
    my_game = Game(game_players, game_shop)
    return my_game

def simulate_games(num_players, player_types, num_games):
    randomania_decks = []
    miser_decks = []
    common_sense_decks = []
    for i in range(num_games):
        if i%50 == 0 and i != 0:
            print('simulated ' + str(num_games) + ' games so far')

        game = start_game(num_players, player_types)
        for x in game.players:
            x.join_game(game)
            random.shuffle(x.my_deck.draw_pile)
            x.my_deck.draw(5)
        while not game.game_over:
            game.active_player.play_actions(game.active_player.my_deck.get_actions_in_hand())
            game.active_player.buy_cards()
            game.next_turn()
        for x in game.players:
            if x.ai.name == 'miser':
                miser_decks += [[x.count_points(), x.my_deck.get_all_card_names()]]
            elif x.ai.name == 'common-sense':
                common_sense_decks += [[x.count_points(), x.my_deck.get_all_card_names()]]
            elif x.ai.name == 'random':
                randomania_decks += [[x.count_points(), x.my_deck.get_all_card_names()]]
        

    randomania_decks = sorted(randomania_decks)
    miser_decks = sorted(miser_decks)
    common_sense_decks = sorted(common_sense_decks)

    miser_sum = 0
    common_sense_sum = 0
    randomania_sum = 0
    for x in range(len(randomania_decks)):
        randomania_sum += randomania_decks[x][0]

    for x in range(len(common_sense_decks)):
        common_sense_sum += common_sense_decks[x][0]

    for x in range(len(miser_decks)):
        miser_sum += miser_decks[x][0]

    if len(miser_decks) != 0:
        print('Miser Avg. Score = ' + str(miser_sum/len(miser_decks)))
    if len(common_sense_decks) != 0:
        print('Common_Sense Avg. Score = ' + str(common_sense_sum/len(common_sense_decks)))
    if len(randomania_decks) != 0:
        print('Randomania Avg. Score = ' + str(randomania_sum/len(randomania_decks)))