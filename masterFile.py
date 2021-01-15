import random as rand
import os
import datetime as dtime
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
        
        def isValuable(self, bestAC, vT):
            # Check if highestCard's rank index is at least greater than 'vT' (value threshold - an int) ranks below bestAC's rank index
            highestCardRI = Deck.ranks.index(self.getRank())
            if(bestAC != "null"):
                bestACRI = Deck.ranks.index(bestAC.getRank())
                if(highestCardRI > (bestACRI - vT)): return True
                else: return False
            else: return True
                        
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
    roundWins = 0
    gameWins = 0
    
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
    
    def addGameWin(self):
        self.gameWins += 1

    def addRoundWin(self):
        self.roundWins += 1
    
    def getGameWins(self):
        return self.gameWins
    
    def getRoundWins(self):
        return self.roundWins
    
    def sortDeck(self, deck, leadingSuit):
        for i in range(len(deck)-1):
            for j in range(len(deck)-1-i):
                if(deck[j].beat(deck[j+1],leadingSuit)):
                    temp = deck[j+1]
                    deck[j+1] = deck[j]
                    deck[j] = temp
    
class HumanPlayer(Player):
    
    def __init__(self,name,hand):
        Player.__init__(self,name,hand)
        
    def displayPlayerHand(self):
        cardsClub = []
        cardsSpade = []
        cardsDiamond = []
        cardsHeart = []
        cards = self.hand.getDeck()
        cardPos = 1
        
        self.sortDeck(cardsClub, '\u2663')
        self.sortDeck(cardsSpade, '\u2660')
        self.sortDeck(cardsDiamond, '\u2666')
        self.sortDeck(cardsHeart, '\u2665')
        
        for card in cards:
            if card.getSuit() == '\u2663':
                cardsClub.append(str(card)+(" [%s]  | "%cardPos))
            elif card.getSuit() == '\u2660':
                cardsSpade.append(str(card)+(" [%s]  | "%cardPos))
            elif card.getSuit() == '\u2666':
                cardsDiamond.append(str(card)+(" [%s]  | "%cardPos))
            else:
                cardsHeart.append(str(card)+(" [%s]  | "%cardPos))
            cardPos += 1

        print('\u2663: ', end='')
        for card in cardsClub:
            print(card, end=" ")
        print("")
        print('\u2660: ', end='')
        for card in cardsSpade:
            print(card, end=" ")
        print("")
        print('\u2666: ', end='')
        for card in cardsDiamond:
            print(card, end=" ")
        print("")
        print('\u2665: ', end='')
        for card in cardsHeart:
            print(card, end=" ")
        print("")
    
    def playCard(self,leadingSuit):
        while(True):
            index = input("\nWhich card to play?(select a [number]): ")
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
   
    randCPUNameBank = ["Joe(CPU)", "Jian-Yang(CPU)", "NOTACPU(CPU)", "You(CPU)", "Big Chungus(CPU)", "Harambe(CPU)", "Chunky Boi(CPU)", "Hugh Mungus(CPU)", "CardSlayer(CPU)", "google_was_my_idea(CPU)","PizzaLeftovers(CPU)", "SunChips(CPU)", "JoeBiden(CPU)", "23904290348(CPU)", "awb9v8rycnw98(CPU)", "PancakesAreBetter(CPU)", "Derp(CPU)", "<InsertCreativeName>(CPU)", "Jimmy(CPU)"]
    s2hDict = {'\u2660':0, '\u2663':1, '\u2665':2, '\u2666':3}  # dictionary converts leadingSuit unicode to corresponding index of suitHand in hand
    h2sDict = {0:'\u2660', 1:'\u2663', 2:'\u2665', 3:'\u2666'}
    
    choice = 0
    cardsPlayed = []
    activeCards = []
    safeCards = []
    
    def __init__(self, name, hand, aF = 0.5, iF = 0.0552, vT = 5):
        Player.__init__(self,name,hand)
        self.aF = aF
        self.iF = iF
        self.vT = vT
    
    def setRandCPUName(self): 
        self.name = rand.choice(self.randCPUNameBank)
        self.randCPUNameBank.remove(self.name)
    
    def taunt(self):
        tauntList = ["Eat this.", "How'd you like them apples?", "Get good.", "Good luck after that.", "Are you all even trying?", "I'd give up if I were you.", "Is this even a competition?", "Run while you can!", "Aww, did I just beat your card?", "What's this? Me winning."]
        tauntActionOff = False
        taunt = rand.choice(tauntList)
        if(tauntActionOff == False):
            if(rand.randint(0,1) == 1): # random chance
                time.sleep(0.75)
                print("\n\"", end = "")
                print(taunt, "\" - ", self.name, end = "")
                time.sleep(0.75)
    
    def endTaunt(self):
        endTauntList = ["\"gg\"", "\"GG\"", "\"Well played, everyone\"", "\":D\"", "\"A fine game this was\""]
        return rand.choice(endTauntList)
    
    def getInfo(self):
        numCards = 0
        for suitHand in self.hand: numCards += len(suitHand.getDeck())
        return 'User: {} | Cards: {}'.format(self.name,numCards)
    
    def getHandStr(self):
        for handSuit in self.hand:
            print(handSuit.getDeckStr())

    def getHandDeck(self):      # return all cards in handSuits
        handDeck = []
        for suitHand in self.hand:
            for card in suitHand.getDeck():
                handDeck.append(card)
        return handDeck
    
    def getPlayerSuits(self):
        suits = []
        for handSuit in self.hand:
            for card in handSuit.getDeck():
                suits.append(card.getSuit())
        return suits

    def setActiveCards(self):
        self.activeCards.clear()
        
        # Count activeCards in game
        for card in Deck().getDeck():
            if(not self.cardsPlayed.__contains__(card) and not self.getHandDeck().__contains__(card)):
                self.activeCards.append(card)
        #print("    DEBUG: acs - %s" % len(self.activeCards))

    def setSafeCards(self, leadingSuit):
        self.safeCards.clear()
        # If plays first, choose suit of most safe cards to play
        if(leadingSuit == "null"):
            for suitHand in self.hand:
                tempSC = []
                currentSuit = self.h2sDict.get(self.hand.index(suitHand))
                bestAC = self.getBestAC(currentSuit)
                #print("    DEBUG: bestAC %s" % bestAC)
                for card in suitHand.getDeck():
                    if(bestAC == "null" or card.beat(bestAC, currentSuit)):
                        tempSC.append(card)
                    
                if(len(tempSC) > len(self.safeCards)):
                    self.safeCards = tempSC
        else:
            bestAC = self.getBestAC(leadingSuit)
            for card in self.hand[self.s2hDict.get(leadingSuit)].getDeck():
                if(bestAC == "null" or card.beat(bestAC, leadingSuit)):
                    self.safeCards.append(card)
            
    def getBestAC(self, leadingSuit):
        bestCard = "null"
        for card in self.activeCards:
            if(card.getSuit() == leadingSuit):
                if(bestCard == "null"):
                    bestCard = card
                elif(card.beat(bestCard, leadingSuit)):
                    bestCard = card
        return bestCard
    
    ''' sort deck goes here '''
        
    def splitHand(self):
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
        leadingSuitHand = self.hand[self.s2hDict.get(highestCard.getSuit())].getDeck()
        index = 0
        for card in leadingSuitHand:
            if(card.beat(highestCard,highestCard.getSuit())): return index
            index += 1
        return -1

    def adjustAF(self, curRound, totRound):   # method increases or decreases aF by a sum created by probability of beneficial or negative environment
        if(curRound > (totRound/3)):
            self.aF += 1
    
    def conditionCPU(self, winningPlayer):
        #print("    DEBUG: Conditioning %s..." % self.name)
        #print("    DEBUG: Current aF: %s" % self.aF)
        if(self.choice == 0):   # if saved
            if(self == winningPlayer):  # and could have won
                self.aF += (self.iF)*1.2
            else:                       # and did not win
                self.aF -= self.iF
        elif(self.choice == 1): # if played
            if(self == winningPlayer):  # and won
                self.aF += self.iF
            else:                       # and lost
                self.aF -= (self.iF)*1.2
        #print("    DEBUG: Adjusted aF: %s" % self.aF)
        
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
        
        ''' Setting first leadingSuit & handSuit to play from '''
        if(leadingSuit == "null"):      # If CPU is playing first
            if(len(self.safeCards) > 1):                # Set suit to surplus cards
                leadingSuit = self.safeCards[0].getSuit()
            else:
                leadingSuit = self.hSF()[0].getSuit()   # Set suit to most frequent cards
            print("%s is now the leading suit" % leadingSuit)
        leadingSuitHand = self.hand[self.s2hDict.get(leadingSuit)].getDeck()  
        
        ''' Decision Making '''
        if(len(leadingSuitHand) > 0):
            #print("    DEBUG: playing leadingsuit")
            # Beginning-turn play (burn surplus)
            if(curTurn == 0 and len(self.safeCards) > 1):
                #print("    DEBUG: playing burn-surp")
                self.choice = 2
                cardChoice = self.safeCards[0]
                leadingSuitHand.remove(cardChoice)
                print(" \u261B   %s played %s" % (self.name, cardChoice))
                self.taunt()
                return cardChoice
            
            # End-turn play
            elif(curTurn == totTurn and self.mWC(highestCard) != -1):         # always wins in end (or add worth evaluation? if num of played hVal cards < totCards)
                #print("    DEBUG: playing mwc-end")
                self.choice = 2                                                 # forced play-win
                cardChoice = leadingSuitHand[self.mWC(highestCard)]
                leadingSuitHand.remove(cardChoice)
                print(" \u261B   %s played %s" % (self.name, cardChoice))
                self.taunt()                                                
                return cardChoice
            
            # Overtake/Bait Play
            elif(highestCard != "null" and self.mWC(highestCard) != -1 and rand.random() < self.aF):
                #overtake - if highest card is valuable (w/ perspective to bestAC), compete for it
                #print("    DEBUG: value - %s > %s = %s" % (Deck.ranks.index(highestCard.getRank()),Deck.ranks.index(self.getBestAC(leadingSuit).getRank())-4,highestCard.isValuable(self.getBestAC(leadingSuit), self.vT)))
                if(highestCard.isValuable(self.getBestAC(leadingSuit), self.vT)):
                    #print("    DEBUG: playing overtake")
                    self.choice = 1
                    ovIndex = self.mWC(highestCard) + (totTurn - curTurn) # increase value of card if further from end of turn (more other player risk)
                    if(ovIndex > len(leadingSuitHand)-1): ovIndex = len(leadingSuitHand)-1 # if index out of range, set to trump card
                    cardChoice = leadingSuitHand[ovIndex]
                    leadingSuitHand.remove(cardChoice)
                    print(" \u261B   %s played %s" % (self.name, cardChoice))
                    return cardChoice
                
                
                #baiting - if highest card is mediocre, raise stakes
                else:
                    #print("    DEBUG: playing bait")
                    self.choice=2
                    cardChoice = leadingSuitHand[self.mWC(highestCard)]
                    leadingSuitHand.remove(cardChoice)
                    print(" \u261B   %s played %s" % (self.name, cardChoice))
                    return cardChoice
            
            else:   
                if(highestCard != "null" and leadingSuitHand[self.mWC(highestCard)].beat(highestCard, leadingSuit)):
                    #print("    DEBUG: playing safe")
                    self.choice = 0   # chose play-save
                else:
                    #print("    DEBUG: forced safe") 
                    self.choice = 2                                                                                     # forced play-save

                for card in leadingSuitHand:    # find first instance of suit card (lowest suit card in sorted list) 
                    if(card.getSuit() == leadingSuit):                         
                        leadingSuitHand.remove(card)
                        print(" \u261B   %s played %s" % (self.name, card))
                        return card
                    
        else:                                                                         # non-obligatory suit (no leadingSuit available to play) card choice
            #print("    DEBUG: forced safe")
            self.choice = 2
            
            cardChoice = self.wSR(leadingSuit).getDeck()[0]
            self.wSR(leadingSuit).getDeck().remove(cardChoice)
            print(" \u261B   %s played %s" % (self.name, cardChoice))
            return cardChoice
    
def secureIntInput(prompt,lb,ub):
    while(True):
        inputStr = input(prompt)
        try:
            inputInt = int(inputStr)
            if(inputInt > lb and inputInt < ub):
                print("\n")
                return inputInt
            else:
                print("Number out of bounds!")
        except:
            print("Enter a number!")
                
def main():
    deck = Deck()
    deck.fillClassic()
    while(True):
        print("\n_____________________________")
        print("")
        print("♢ 🂩 ♧ «< The Game >» ♤ 🂩 ♡")
        print("")
        print("_____________________________\n\n")

        for i in range(500): deck.shuffle()
        
        numPlayers = secureIntInput("Enter number of players: ", 1, 53)
        
        hands = deck.split(numPlayers)      # List of Decks
        totRound = len(hands[0].getDeck())
        
        handNum = secureIntInput("Of the %s hands, which do you want?: " % len(hands), 0, len(hands)+1)-1

        
        print("Your Cards: ")
        hands[handNum].getDeckStr()
        
        players = []
        players.append(HumanPlayer(input("Enter Name: "), hands[handNum]))
        hands.remove(hands[handNum])
        
        for i in range(len(hands)):
            players.append(ComputerPlayer("CPU %s" % (i+1), hands[i]))
            players[i+1].setRandCPUName()   # Change CPU names to random
            players[i+1].splitHand() # Split CPU hands into suitHands
    
        print("\nOur Contenders...")
        for player in players: print(player.getInfo())
        input("\nPress ENTER to continue")
        
        
        #Game Rounds
        print("\n\n\n🂩  «Start!» 🂩\n")
        print("__________________")
        time.sleep(0.7)
        
        
        rand.shuffle(players)
        totTurn = len(players)-1
        cardsPlayed = []
        for curRound in range(totRound):
            highestCard = "null"
            leadingSuit = "null"
            
            print("\n\n-= Round %i =-" % (curRound+1))
            time.sleep(0.35)
            
        
            #Game Turns
            curTurn = 0
            for player in players:
                print("\n%s's Turn." % player)
                
                # Human Move
                if(isinstance(player,HumanPlayer)):
                    print("Your hand\n")
                    if(leadingSuit == "null"): print("Leading Suit: Your call")
                    else: print("Leading Suit: %s" % leadingSuit)
                    player.displayPlayerHand()
                    cardChoice = player.playCard(leadingSuit)
                
                # Computer Move
                else:
                    player.adjustAF(curRound, totRound)
                    player.cardsPlayed = cardsPlayed
                    player.setActiveCards()
                    player.setSafeCards(leadingSuit)
    
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
            winningPlayer.addGameWin()
            
            for player in players:
                if(isinstance(player, ComputerPlayer)):
                    player.conditionCPU(winningPlayer)
            
            winningPlayer.addRoundWin()
            print("\n\n\n%s Won the Round! %s goes next..." % (winningPlayer,winningPlayer))        
            time.sleep(1)
        
        winner = player
        for player in players:
            if(player.getGameWins() > winner.getGameWins()): winner = player
        
        winner.addGameWin()
        print("-= Game Over! =-")
        time.sleep(1.5)
        print("The Winner is...", end = "")
        time.sleep(2)   
        print(" %s! Won by %s points" % (winner,winner.getGameWins()))
        time.sleep(1)
        print("\n- Player Chart -")
        for player in players:
            print("%s - %s pts" % (player.name,player.getGameWins()))
        
        print("\n\n")
        for player in players:
            if(isinstance(player,ComputerPlayer)):
                time.sleep(1)
                print("%s - %s" % (player.endTaunt(), player.name))
        
        gameInput = input("Play a Rematch? (Yes/No):  ")
        if(gameInput == "No" or gameInput == "no"):
            break
        
    if(os.path.exists("gamestatus.txt")):
        gfi = open("gamestatus.txt", "a")
    else:
        gfi = open("gamestatus.txt", "x")
        gfi.write("            -= Game Stats =-\n")

    for player in players:
        if(isinstance(player,HumanPlayer)): human = player
    gfi.write("\nName: %s" % human.name)
    gfi.write("\nGame Date: %s" % dtime.datetime.now())
    gfi.write("\nRounds Won: %s" % human.roundWins)
    gfi.write("\nGames Won: %s" % human.gameWins)
    gfi.write("\n===============\n")
    gfi.close()
    




if __name__=='__main__':
    main()