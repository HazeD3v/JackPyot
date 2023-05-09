import random

#Set the Symbols, their frequency and an example start screen
symbols = ['7', '!', '#', '@',]
symbol_freq = { '7': 3, '!': 4, '#': 4, '@': 4 }
symbol_payout = { '7': 10, '!': 5, '#': 3, '@': 2 }
start_screen = [['?','?','?'],['?', '?', '?'],['?', '?', '?']]


def getBalance():
    """Gets deposit amount from user"""
    while True:
        amount = input("How much do you want to deposit? \n$ ")
        if amount.isdigit():
            break
        else:
            print("[x] Enter a valid deposit amount. [x]")
    return int(amount)


def getLines():
    """Gets number of lines to bet on from user"""
    while True:
        lineAmount = input("Enter amount of lines to bet on. (Min: 1, Max: 3\n# ")
        if lineAmount.isdigit():
            if 0 <= int(lineAmount) <= 3:
                break
            else:
                print("[x] Minimum is 1 Maximum is 3. (1-3) [x]")
        else:
            print("[x] Enter a valid amount of lines. (1-3) [x]")

    return int(lineAmount)


def getBetAmount(bal, lAmount):
    """Gets bet amount from user"""
    while True:
        betAmount = input("Enter amount to bet on each line. (Min: 1, Max: 50)\n# ")
        if betAmount.isdigit():
            if 0 <= int(betAmount) <= 50:
                if (int(betAmount)*int(lAmount)) <= int(bal):
                    break
                else:
                    print(f"[x] You do not have enough funds![x]\nBalance: {bal}")
            else:
                print("[x] Minimum is 1 Maximum is 50. [x]")
        else:
            print("[x] Enter a valid amount to bet. (1-50)[x]")

    return int(betAmount)


def getBetConf(bal, lAmount, bAmount, tbAmount):
    """Displays information about current bet and asks for confirmation"""
    print("\n[!] Bet Information. [!]")
    print(f"Your balance is: {bal}")
    print(f"Amount of lines: {lAmount}")
    print(f"Bet amount per line: {bAmount}")
    print(f"Your total bet is: {tbAmount}")
    print(f"Balance after spin: {int(bal) - int(tbAmount)}")
    while True:
        confirm = input("Do you want to confirm and spin? (y/n) ")
        if confirm == "y":
            return 'y'
        else:
            return 'n'


def getSpinScreen(symbols, freq, screen):
    """Returns a matrix of symbol results"""
    results = [[],[],[]]
    for i, col in enumerate(screen):    # x3 reults
        for _ in col:                   # x3 results
            while True:
                #pick a random symbol from symbol list
                new_symbol = random.choice(symbols)
                # if the symbol has available symbols to give
                if freq.get(new_symbol) > 0:
                    #Append the result to results matrix
                    results[i].append(new_symbol)
                    freq[new_symbol] -= 1
                    break
    
    return results


def printResultScreen(m, bAmount, tbet, payList):
    """
    Prints result of slot game and returns total winnings

    Todo:
    ~ Need to add the option to only payout for certain lines as indicated by the user (lineAmount) in getLines()
    ~ Display output in a readble friendly way.
    ~ Display Slot results a bit nicer instead of just a list being printed 
    """
    row1 = [row[0] for row in m]
    row2 = [row[1] for row in m]
    row3 = [row[2] for row in m]
    winCount = 0
    winSymbols = []
    winLines = []
    #Left to Right same row Payout- Top
    if row1[0] == row1[1] and row1[1] == row1[2]:
        print("==  Winner!!!  ==")
        winCount += 1
        winSymbols.append(row1[0])
        winLines.append('Top Row Line')
    
    #Left to Right same row Payout- Middle
    if row2[0] == row2[1] and row2[1] == row2[2]:
        print("==  Winner!!!  ==")
        winCount += 1
        winSymbols.append(row2[0])
        winLines.append('Middle Row Line')
    
    #Left to Right same row Payout- Bottom
    if row3[0] == row3[1] and row3[1] == row3[2]:
        print("==  Winner!!!  ==")
        winCount += 1
        winSymbols.append(row3[0])
        winLines.append('Bottom Row Line')
    
    #Top Left to Bottom Right Diagonal Payout
    if row1[0] == row2[1] and row2[1] == row3[2]:
        print("==  Winner!!!  ==")
        winCount += 1
        winSymbols.append(row1[0])
        winLines.append('Top Left Diagonal Line')

    #Bottom Left to Top Right Diagonal Payout
    if row3[0] == row2[1] and row2[1] == row1[2]:
        print("==  Winner!!!  ==")
        winCount += 1
        winSymbols.append(row3[0])
        winLines.append('Bottom Left Diagonal Line')

    totalWin = 0
    if len(winSymbols) > 0:
        for win in winSymbols:
            totalWin += (int(payList[win]) * int(bAmount))

    print(winCount)
    print(winSymbols)
    print(winLines)
    print(f"Total winnings: {totalWin}")
    print(f"{row1}\n{row2}\n{row3}")
    return int(totalWin)


def slots(bal):
    """This slot function runs the slot and returns"""
    lines = getLines()
    betAmount = getBetAmount(bal, lines)
    totalBet = int(lines) * int(betAmount)
    conf = getBetConf(bal, lines, betAmount, totalBet)
    if conf == 'y':
        print("Spin!!\n")
        bal = int(bal) - int(totalBet)
        print(f"Balance after spin: {bal}")
        
        symFreq = symbol_freq.copy()
        matrix = getSpinScreen(symbols, symFreq, start_screen)
        winAmount = printResultScreen(matrix, betAmount, totalBet, symbol_payout)

        return (int(winAmount) + int(bal))
    else:
        print("[x] Bet Cancelled. [x]")
        return int(bal)


def main():
    """The main loop for the game, gets balance and sends it to slots()"""
    balance = getBalance()
    while True:
        if int(balance) > 0:
            print(f"Your balance is ${balance}.")
            play = input("Press enter to play. (q to quit) ")
            if play == 'q':
                break
            balance = slots(balance)
        else:
            print( "[x] No funds! [x]" )
            return


if __name__ == "__main__":
    main()
