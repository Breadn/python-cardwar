import random as rand
import time

class Deck:
    class Card:

        def __init__(self,suit,rank):
            self.suit = suit
            self.rank = rank
        
        def __str__(self):
            return "{} of {}".format(self.rank,self.suit)
        
        def beat(self, other, leadingSuit):
            if((self.suit == leadingSuit and other.suit == leadingSuit) or (self.suit != leadingSuit and other.suit != leadingSuit)):
                return Deck().getRankIndex(self.rank) > Deck().getRankIndex(other.rank) # Call nested class method with class()
            elif(self.suit == leadingSuit):
                return True
            return False
        
        def getSuit(self):
            return self.suit
        
        def getRank(self):
            return self.rank
        
    spade = '\u2660'
    club = '\u2663'
    heart = '\u2665'
    diamond = '\u2666'
    
    suits = [spade, club, heart, diamond]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    deck = []
    
    def __init__(self,deck=[]):
        self.deck = deck
    
    def addCard(self,Card):
        self.deck.append(Card)
    
    def fillClassic(self):
        for suit in self.suits:
            for rank in self.ranks:
                self.addCard(self.Card(suit,rank))
                
    def shuffle(self):
        for i in range(len(self.deck)):
            randIndex = rand.randint(i,len(self.deck)-1)
            temp = self.deck[randIndex]
            self.deck.remove(temp)
            self.deck.insert(i,temp)
            
    def split(self,n=4):
        partSize = int(len(self.deck)/n)
        parts = []
        for i in range(n):
            start = i*partSize
            end = start+partSize
            parts.append(Deck(self.deck[start:end]))    # Changed creating list of lists to list of Decks
        return parts
    
    def getDeckStr(self):
        for card in self.getDeck(): print(card, end=" [%s] |" % (self.getDeck().index(card)+1))
        print("\n")
        
    def getDeck(self):
        return self.deck
    
    def getRankIndex(self,rank):
        return self.ranks.index(rank)
        
class Player:
    numWins = 0
    
    def __init__(self,name,hand):
        self.name = name
        self.hand = hand
    
    def __str__(self):
        return self.name
    
    def getInfo(self):
        return 'User: {} | Cards: {}'.format(self.name,len(self.hand.getDeck()))
    
    def getPlayerSuits(self):
        suits = [card.getSuit() for card in self.hand.getDeck()]
        return suits
    
    def addWin(self):
        self.numWins += 1
    
    def getWins(self):
        return self.numWins
        
class HumanPlayer(Player):
    
    def __init__(self,name,hand):
        Player.__init__(self,name,hand)
    
    def playCard(self,leadingSuit):
        while(True):
            index = input("\nWhich card to play?: ")
            try:
                index = abs(int(index)-1)
                try:
                    card = self.hand.getDeck()[index]
                    if(leadingSuit != "null" and super().getPlayerSuits().__contains__(leadingSuit) and card.getSuit() != leadingSuit):            # Call superclass suits method?
                        print("Please play a card matching the current leading suit.")
                        continue
                    print(" \u261B   You played %s" % card)
                    self.hand.getDeck().remove(card)
                    return card
                except: print("That card is not in your hand!")
            except: print("Choose a valid index!") 
                
class ComputerPlayer(Player):
    '''
    Notes
        - hand is a list of decks split into respective suits, follows SCHD order
            + hand[0] = spades
            + hand[1] = clubs
            + hand[2] = hearts
            + hand[3] = diamonds
            
    # 0 - save,     1 - play,     2 - forcedSave,     3 - forced play (only if applicable w/o bait checking)
    
    '''
   
    suit2handDict = {'\u2660':0, '\u2663':1, '\u2665':2, '\u2666':3}  # dictionary converts leadingSuit unicode to corresponding index of suitHand in hand
    choice = 0
    cardsPlayed = []
    activeCards = []
    
    def __init__(self, name, hand, aF=0.5, iF=0.0552):
        Player.__init__(self,name,hand)
        self.aF = aF
        self.iF = iF
        
    def getInfo(self):
        numCards = 0
        for suitHand in self.hand: numCards += len(suitHand.getDeck())
        return 'User: {} | Cards: {}'.format(self.name,numCards)
    
    def getHandStr(self):
        for handSuit in self.hand:
            print(handSuit.getDeckStr())

    def getPlayerSuits(self):
        suits = []
        for handSuit in self.hand:
            for card in handSuit.getDeck():
                suits.append(card.getSuit())
        return suits

    def getActiveCards(self):
        self.activeCards.clear()
        for card in Deck().getDeck():
            if(not self.cardsPlayed.__contains__(card) and not self.getHandDeck().__contains__(card)):
                self.activeCards.append(card)
        print("    DEBUG: acs - %s" % len(self.activeCards))

    def getHandDeck(self):  	# return all cards in handSuits
        handDeck = []
        for suitHand in self.hand:
            for card in suitHand.getDeck():
                handDeck.append(card)
        return handDeck

    def sortHand(self):
        sortDeck = self.hand.getDeck()
        for i in range(len(sortDeck)-1):
            for j in range(len(sortDeck)-1-i):
                if(sortDeck[j].beat(sortDeck[j+1],'\u2660')):
                    temp = sortDeck[j+1]
                    sortDeck[j+1] = sortDeck[j]
                    sortDeck[j] = temp
        self.hand = Deck(sortDeck)
        
        # split hand into respective suits
        suitHand = []
        for suit in Deck.suits:
            temp_suitHand = Deck(deck=[])
            for card in self.hand.getDeck():
                if(card.getSuit() == suit):
                    temp_suitHand.addCard(card)
            suitHand.append(temp_suitHand)
        
        self.hand = suitHand

    def hSF(self):  	# return suit of highest frequency
        existingSuits = []      # check for non-empty suitHands
        for suitHand in self.hand:
            if(len(suitHand.getDeck()) > 0): existingSuits.append(suitHand)
            
        highestFreq = existingSuits[0].getDeck()
        for i in range(1,len(existingSuits)):
            if(len(existingSuits[i].getDeck()) > len(highestFreq)):
                highestFreq = existingSuits[i].getDeck()
        return highestFreq

    def wSR(self, leadingSuit):      # return suit of worst rank
        existingSuits = []      # check for non-empty suitHands
        for suitHand in self.hand:
            if(len(suitHand.getDeck()) > 0): existingSuits.append(suitHand)
            
        WCSuit = existingSuits[0]        # set initial worst card suit to first suitHand
        for i in range(1,len(existingSuits)):
            otherSuitWC = existingSuits[i].getDeck()[0]     # other suit's worst card
            if(WCSuit.getDeck()[0].beat(otherSuitWC, leadingSuit)): WCSuit = existingSuits[i]
        return WCSuit
    
    def mWC(self, highestCard):     # return index of first instance of minimally winning card 
        leadingSuitHand = self.hand[self.suit2handDict.get(highestCard.getSuit())].getDeck()
        index = 0
        for card in leadingSuitHand:
            if(card.beat(highestCard,highestCard.getSuit())): return index
            index += 1
        return -1

    def adjustAF(self):   # method increases or decreases aF by a sum created by probability of beneficial or negative environment
        pass
    
    def conditionCPU(self, winningPlayer):
        print("    DEBUG: Conditioning %s..." % self.name)
        print("    DEBUG: Current aF: %s" % self.aF)
        if(self.choice == 0):   # if saved
            if(self == winningPlayer):  # and could have won
                self.aF += (self.iF)*1.2
            else:                       # and did not win
                self.aF -= self.iF
        elif(self.choice == 1): # if trump
            if(self == winningPlayer):  # and won
                self.aF += self.iF
            else:                       # and lost
                self.aF -= (self.iF)*1.2
        print("    DEBUG: Adjusted aF: %s" % self.aF)
        
    def playCPU(self, leadingSuit, highestCard, curTurn, totTurn):
        # Current CPU Rules:
        #choose  than any card in play
        #    if none in suit, play lowest
        #    if none higher, play lowest
        #    aggressivity factor, based on probability / cards in play / cards played / current turn ???
        #        + rand<aF = True, rand>aF = False
        # aggressivity factor will also determine rank of high value card to be played (i.e. aF will not determine whether trump card is played)
        # **TO-ADD
        #    Function that tweaks aF based on given environment
        #        - at beginning of round, aF will be 0% and never try trump carding
        #        - if decides to play this round:
        #            + the further away it is from being the last to play, the more valuable of a card it will play that can overtake (does not necessarily mean trump card)
        #              meaning, CPU will not play card to necessarily win, but to also entice other player to play a more valuable card in order to overtake,
        #              giving CPU leeway to play
        #        - if has more than one winnable card out of all remaining cards in play, burn some
        
        if(leadingSuit == "null"):      # If CPU is playing first, choose to make leadingSuit to be from their biggest suit
            leadingSuit = self.hSF()[0].getSuit()
            print("%s is now the leading suit" % leadingSuit)
        
        leadingSuitHand = self.hand[self.suit2handDict.get(leadingSuit)].getDeck()  
        
        if(len(leadingSuitHand) > 0):
            print("    DEBUG: playing leadingsuit")
            trumpCard = leadingSuitHand[len(leadingSuitHand)-1]
                    
            if(curTurn == totTurn and self.mWC(highestCard) != -1):         # always wins in end (or add worth evaluation? if num of played hVal cards < totCards)
                print("    DEBUG: playing mwc-end")
                self.choice = 3                                                 # forced play-win
                cardChoice = leadingSuitHand[self.mWC(highestCard)]
                leadingSuitHand.remove(cardChoice)
                print(" \u261B   %s played %s" % (self.name, cardChoice))                                                
                return cardChoice
            
            # aF w/ intent to make a play (aggressive / baiting) [will not make aggressive play in beginning, until surplusBurn is implemented!!!]
            elif(highestCard != "null" and self.mWC(highestCard) != -1 and rand.random() < self.aF):        # EDIT: leadingSuitHand[self.mWC(highestCard)].beat(highestCard,leadingSuit)
                #aggressive
                if(curTurn != totTurn and trumpCard.beat(highestCard, leadingSuit)):        # never trumps in beginning
                    print("    DEBUG: playing trump")
                    self.choice = 1                                                 # chose to play-win 
                    leadingSuitHand.remove(trumpCard)
                    print(" \u261B   %s played %s" % (self.name, trumpCard))
                    return trumpCard
                
                #baiting
                else:     # (plays just barely above current winning card, higher towards end of turn)
                    print("    DEBUG: playing bait")
                    
                    '''    TEMP PLACEHOLDER BELOW    '''
                    
                    cardChoice = leadingSuitHand[self.mWC(highestCard)]
                    leadingSuitHand.remove(cardChoice)
                    print(" \u261B   %s played %s" % (self.name, cardChoice))                                                
                    return cardChoice
            
            else:
                if(highestCard != "null" and leadingSuitHand[self.mWC(highestCard)].beat(highestCard, leadingSuit)):
                    print("    DEBUG: playing safe")
                    self.choice = 0   # chose play-save
                else:
                    print("    DEBUG: forced safe") 
                    self.choice = 3                                                                                     # forced play-save

                for card in leadingSuitHand:    # find first instance of suit card (lowest suit card in sorted list) 
                    if(card.getSuit() == leadingSuit):                         
                        leadingSuitHand.remove(card)
                        print(" \u261B   %s played %s" % (self.name, card))
                        return card
                    
        else:                                                                         # non-obligatory suit (no leadingSuit available to play) card choice
            print("    DEBUG: forced safe")
            self.choice = 3
            
            cardChoice = self.wSR(leadingSuit).getDeck()[0]
            self.wSR(leadingSuit).getDeck().remove(cardChoice)
            print(" \u261B   %s played %s" % (self.name, cardChoice))
            return cardChoice
        
                
def main():
    print("\n\n♢ 🂩 ♧ « The Game » ♤ 🂩 ♡\n")
    deck = Deck()
    deck.fillClassic()
    deck.shuffle()

    numPlayers = int(input("Enter # of Players: "))
    
    hands = deck.split(numPlayers)      # List of Decks
    rounds = len(hands[0].getDeck())
    handNum = int(input("Of the %s hands, which do you want?: " % len(hands)))-1
    print("Your Cards: ")
    hands[handNum].getDeckStr()
    
    players = []
    players.append(HumanPlayer(input("Enter Name: "), hands[handNum]))
    hands.remove(hands[handNum])
    
    for i in range(len(hands)):
        players.append(ComputerPlayer("CPU %s" % (i+1), hands[i]))
        players[i+1].sortHand() # Sort CPU hands

    print("\nOur Contenders...")
    for player in players: print(player.getInfo())
    input("\nPress ENTER to continue")
    
    
    
    
    #Game Rounds
    print("\n🂩 «Start!» 🂩\n")
    time.sleep(0.7)
    
    
    rand.shuffle(players)
    totTurn = len(players)-1
    cardsPlayed = []
    for currentRound in range(rounds):
        highestCard = "null"
        leadingSuit = "null"
        
        print("\n\n-= Round #%i =-" % (currentRound+1))
        time.sleep(0.35)
        
    
        #Game Turns
        curTurn = 0
        for player in players:
            print("\n%s's Turn." % player)
            
            # Human Move
            if(isinstance(player,HumanPlayer)):     
                print("Your hand\n")
                player.hand.getDeckStr()
                cardChoice = player.playCard(leadingSuit)
            
            # Computer Move
            else:   
                player.cardsPlayed = cardsPlayed
                player.getActiveCards()
                print("%s is choosing..." % player)
                time.sleep(rand.randint(1,4))  # Simulate thinking time
                cardChoice = player.playCPU(leadingSuit, highestCard, curTurn, totTurn)                                
                time.sleep(0.5)
            
            
            # Compete conditions
            if(highestCard == "null"):  # If first card, set it as base card to compete again 
                highestCard = cardChoice
                leadingSuit = cardChoice.getSuit()
                winningPlayer = player
                
            elif(cardChoice.beat(highestCard, leadingSuit)):
                highestCard = cardChoice
                winningPlayer = player
            
            cardsPlayed.append(cardChoice)
            curTurn += 1
            time.sleep(1)
        
        time.sleep(0.5)
        players.remove(winningPlayer)
        players.insert(0,winningPlayer)
        winningPlayer.addWin()
        
        for player in players:
            if(isinstance(player, ComputerPlayer)):
                player.conditionCPU(winningPlayer)
        print("\n\n\n%s Won the Round! %s goes next..." % (winningPlayer,winningPlayer))        
        time.sleep(1)
    
    winner = player
    for player in players:
        if(player.getWins() > winner.getWins()): winner = player
        
    print("-= Game Over! =-")
    time.sleep(1.5)
    print("The Winner is...", end = "")
    time.sleep(2)   
    print(" %s! Won by %s points" % (winner,winner.getWins()))
    time.sleep(1)
    print("\n- Player Chart -")
    for player in players:
        print("%s - %s pts" % (player.name,player.getWins()))
    
    if input("Would you like to play another game?(Yes/No): ") == "Yes" or "yes": 
        main()
            
        
    




if __name__=='__main__':
    main()