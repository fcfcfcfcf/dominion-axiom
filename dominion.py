import random
import re

##### REGEX DEFS ######
basic_action_regex = re.compile("^\+(.) (.*)$")

#######################




################### CLASSES #########################
class Game:
    def __init__(self, my_players, my_shop):
        self.players = my_players
        for x in self.players:
            x.join_game(self)
        self.num_players = len(self.players)
        self.trash = []
        self.active_player = self.players[0]
        self.active_player_number = 0
        self.shop = my_shop
        self.game_over = False
        self.empty_piles_needed = 4

    def play_card(self, card):
        self.active_player.deck.hand.remove(card)
        self.active_player.deck.in_play.append(card)
        if card.is_attack:
            self.process_card_actions(card.actions, None)
            self.process_attack(card.additional_action)
        else:
            self.process_card_actions(card.actions, card.additional_action)

    def buy_card(self, card):
        for_sale = self.shop.shop_contents
        if for_sale[card.name] != 0:
            for_sale[card.name] -= 1
            if for_sale[card.name] == 0:
                self.shop.empty_piles += 1


    def process_card_actions(self, actions, additional_action):
        for x in actions:
            actual_action = basic_action_regex.match(x)
            amount = actual_action.group(1)
            act_type = actual_action.group(2)
            if act_type == 'Card' or act_type == 'Cards':
                self.active_player.draw(amount)
            elif act_type == 'Buy' or act_type == 'Buys':
                self.active_player.buys += amount
            elif act_type == 'Action' or act_type == 'Actions':
                self.active_player.actions += amount
            elif act_type == 'Coin' or act_type == 'Coins':
                self.active_player.coins += amount

        additional_action(self)

    def process_reaction(self, react_fn):
        return react_fn(self)
        #reactions return True if they negate the attack completely

    def process_attack(self, attack_fn):
        for x in self.players:
            reactions = x.deck.get_reactions_in_hand()
            blocked = False
            if reactions != None:
                for y in reactions:
                    if self.process_reaction(y):
                        blocked = True
            if not blocked:
                attack_fn(self, x)
    
    def next_turn(self):
        self.active_player.cleanup()
        if(self.empty_piles_needed <= self.shop.empty_piles):
            self.game_over = True
            return True
        else:
            self.active_player_number = (self.active_player_number + 1) % self.num_players
            self.active_player = self.players[self.active_player_number]
            return False


class Shop:
    def __init__(self, my_supply_dict):
        self.supply = my_supply_dict
        self.empty_piles = 0

    def get_cards_under_amount(self, amount):
        cards_under_amount = []
        for x in self.supply:
            if x[0].cost <= amount:
                cards_under_amount += x[0]
        return cards_under_amount


class Card:
    def __init__(self, my_base_actions, my_cost, my_pts, my_worth, my_additional_action, _is_attack, _is_reaction, my_reaction, my_name):
        self.actions = my_base_actions
        self.cost = my_cost
        self.pts = my_pts
        self.worth = my_worth
        self.additional_action = my_additional_action
        self.is_attack = _is_attack
        self.is_reaction = _is_reaction
        self.reaction = my_reaction
        self.name = my_name

class Player:
    def __init__(self, starting_deck, my_name, decision_dict):
        self.my_deck = starting_deck
        self.name = my_name
        self.actions = 1
        self.buys = 1
        self.coins = 0
        self.game = None
        self.decisions = decision_dict

    def join_game(self, game_to_join):
        self.game = game_to_join

    def play_actions(self, action_cards):
        if self.actions > 0:
            action_to_play = self.decisions['actions'](self.my_deck, action_cards)
            if action_to_play.name != 'error': 
                self.game.play_card(action_to_play)
                self.actions -= 1
                self.play_actions(action_cards - action_to_play)
    
    def buy_cards(self):
        self.coins += self.my_deck.hand.calc_hand_value()
        if self.buys > 0:
            card_to_buy = self.decisions['buy'](self.game.shop, self.my_deck, self.coins)
            if card_to_buy.name != 'error':
                self.game.buy_card(card_to_buy)
                self.coins -= card_to_buy.cost
                self.buys -= 1
                self.my_deck.discard_pile += card_to_buy
                self.buy_cards()

    def choose_card_to_discard(self):
        self.my_deck.discard(self.decisions['discard'](self.my_deck))
        
    def cleanup(self):
        self.my_deck.cleanup_deck_actions()
        self.actions = 1
        self.buys = 1
        self.coins = 0

class Deck:
    def __init__(self, my_cards):
        self.cards = my_cards
        self.draw_pile = []
        self.discard_pile = []
        self.hand = []
        self.in_play = []

    def shuffle(self):
        self.draw_pile = self.draw_pile + random.shuffle(self.discard_pile)
        self.discard_pile = []

    def cleanup_deck_actions(self):
        self.discard_pile = self.discard_pile + self.hand + self.in_play
        self.hand = []
        self.in_play = []
        self.draw(5)

    def draw(self, amnt):
        if len(self.draw_pile) < 5:
            self.shuffle()
        for i in range(amnt):
            self.hand += self.draw_pile.pop()

    def discard(self, cards):
        for x in cards:
            self.hand.remove(x)
            self.discard_pile.append(x)

    def place(self, card, offset):
        self.draw_pile.insert(card, offset)

    def calc_hand_value(self):
        total_value = 0
        for x in self.hand:
            total_value += x.worth
        return total_value
    
    def get_actions_in_hand(self):
        my_hand_actions = []
        for x in self.hand:
            if x.actions != None:
                my_hand_actions += x
        return my_hand_actions

    def get_reactions_in_hand(self):
        my_hand_reactions = []
        for x in self.hand:
            if x._is_reaction:
                my_hand_reactions += x
        return my_hand_reactions

#########################################################

############# RANDOM DECISION FUNCTIONS #############
imaginary_card = Card(None, 0, 0, 0, None, False, False, None, 'error')
def random_action(_deck, _actions):
    return random.choice(_actions + imaginary_card)

def random_discard(_deck):
    return random.choice(_deck.hand)

def random_discard_option(_deck):
    return random.choice(_deck.hand + imaginary_card)

def random_buy(_shop, _deck, _coins):
    cards_available = _shop.get_cards_under_amount(_coins)
    return random.choice(cards_available + imaginary_card)

def random_trash(_self, _deck, _coins):
    return random.choice(_deck.hand)

def random_trash_for_treasure(_shop, _deck, _coins):
    treasures = []
    for x in _deck.hand:
        if x.worth > 0:
            treasures += x
    treasures += imaginary_card
    treasure_to_trash = random.choice(treasures)
    return treasure_to_trash
    
def random_gain(_shop, _deck, _limit, _worth_limit):
    cards_available = []
    for x in _shop.supply:
        if x[0].cost <= _limit:
            if x[0].worth <= _worth_limit:
                cards_available += x[0]
    return random.choice(cards_available)


randomania = {}
randomania['discard'] = random_discard
randomania['discard-option'] = random_discard_option
randomania['buy'] = random_buy
randomania['action'] = random_action
randomania['trash'] = random_trash
randomania['trash-treasure'] = random_trash_for_treasure
randomania['gain'] = random_gain

#####################################################

####### GAME CARDS (& thier additonal actions) ###########

copper = Card(None, 0, 0, 1, None, False, False, None, 'copper')
silver = Card(None, 3, 0, 2, None, False, False, None, 'silver')
gold = Card(None, 6, 0, 3, None, False, False, None, 'gold')
curse = Card(None, 0, -1, 0, None, False, False, None, 'curse')
estate = Card(None, 2, 1, 0, None, False, False, None, 'estate')
duchy = Card(None, 5, 3, 0, None, False, False, None, 'duchy')
province = Card(None, 8, 6, 0, None, False, False, None, 'province')

def cellar_action(my_game):
    cur_player = my_game.active_player
    cards_to_discard = []
    targ_card = random_discard_option(cur_player.deck)
    while targ_card.name != 'error':
        cards_to_discard += targ_card
        cur_player.discard(targ_card)
        targ_card = random_discard_option(cur_player.deck)
    cur_player.draw(len(cards_to_discard))

cellar = Card(['+1 Action'], 2, 0, 0, cellar_action, False, False, None, 'cellar')
market = Card(['+1 Card', '+1 Action', '+1 Buy', '+1 Coin'], 5, 0, 0, None, False, False, None, 'market')

def merchant_action(my_game):
    cur_player = my_game.active_player
    if silver in cur_player.hand:
        my_game.process_card_actions('+1 Coin', None)

merchant = Card(['+1 Card', '+1 Action'], 3, 0, 0, merchant_action, False, False, None, 'merchant')

def militia_action(my_game, target_player):
    while len(target_player.my_deck.hand) > 3:
        target_player.choose_card_to_discard()

militia = Card(['+2 Coins'], 4, 0, 0, militia_action, True, False, None, 'militia')

def mine_action(my_game):
    card = my_game.active_player.decisions['trash-treasure'](my_game.shop, my_game.active_player.my_deck, my_game.active_player._coins)
    if card.name != 'error':
        card_to_gain = my_game.active_player.decisions['gain']

#####################################################



GENERIC_STARTING_DECK = [copper, copper, copper, copper, copper, copper, copper, estate, estate, estate]
GENERIC_DECISION_DICT = randomania

################    SHOP    #########################
shop_contents = {}
shop_action_amount = 10
shop_vp_amount = 12
shop_contents['copper'] = [copper, 60]
shop_contents['silver'] = [silver, 40]
shop_contents['gold'] = [gold, 30]
shop_contents['curse'] = [curse, 30]
shop_contents['estate'] = [estate, shop_vp_amount]
shop_contents['duchy'] = [duchy, shop_vp_amount]
shop_contents['province'] = [province, shop_vp_amount]
shop_contents['cellar'] = [cellar, shop_action_amount]
shop_contents['market'] = [market, shop_action_amount]
shop_contents['merchant'] = [merchant, shop_action_amount]
shop_contents['militia'] = [militia, shop_action_amount]
shop_contents['mine'] = [mine, shop_action_amount]
shop_contents['moat'] = [moat, shop_action_amount]
shop_contents['remodel'] = [remodel, shop_action_amount]
shop_contents['smithy'] = [smithy, shop_action_amount]
shop_contents['village'] = [village, shop_action_amount]
shop_contents['workshop'] = [workshop, shop_action_amount]

#####################################################


def start_game(num_players):
    game_players = []
    for x in range(len(num_players)):
        game_players += Player(GENERIC_STARTING_DECK, 'player' + str(x), randomania)
        