import socket
import pickle # sending objects

from gameboard import BoardClass

def reconnect_request(answer) -> str:
    """Allow the user to choose whether they want to attempt another connection or not.

    Args:
        answer: The prior user decision on whether they want to connect again.
    
    Returns:
        answer (str): The user decision on whether they want to connect again.
    """
    connection_query = input("Failed to connect. Do you want to try connecting again? (Y/N): ").capitalize()
    if connection_query == "N":
        exit()
    else:
        answer = connection_query
        return answer

continue_connection = "Y"
while continue_connection == "Y":
    try:
        # prompt user to enter IP address and port
        IP_address = input("Enter an IP address: ")
        port = int(input("Enter a port: "))
        # make the connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Attempting to connect...")
        s.connect((IP_address, port))
        print("\nConnected!")
        break
    except ConnectionRefusedError:
        reconnect_request(continue_connection)
    except TimeoutError:
        reconnect_request(continue_connection)
    except ValueError:
        reconnect_request(continue_connection)
    except OSError:
        reconnect_request(continue_connection)

# send username
user_name = input("Please enter your username: ")
s.send(user_name.encode())

# receive the other username
player2_name = s.recv(1024)
player2_name = player2_name.decode()

o_player = BoardClass("X", user_name, " ")

play_again = True

while play_again == True:
    o_player.updateGamesPlayed()
    
    while o_player.isWinner("X") == False and o_player.isWinner("O") == False and o_player.boardIsFull() == False:
        print("It is now your turn to play.")
        o_player.print_board()
        keypad = int(input("Enter a number 1-9: "))
        keypad -= 1
        o_player.edit_board(keypad)

        o_player.print_board()

        o_board = pickle.dumps(o_player.board)
        s.send(o_board)

        if o_player.isWinner("X") == True or o_player.boardIsFull() == True:
            o_player.lastTurnName(user_name)
            break

        print("\nWaiting for the other player.")
        x_board = s.recv(1024)
        x_board = pickle.loads(x_board)
        o_player.updateGameBoard(x_board)

        o_player.lastTurnName(player2_name)

    if o_player.isWinner("X") == True:
        o_player.updateWins()
        print("Hooray, you won the game!")
    elif o_player.boardIsFull() == True and o_player.isWinner("O") != True:
        o_player.updateTies()
        print("Aw, it is a draw.")
    else:
        o_player.updateLosses()
        print("Darn, " + player2_name + " won.")

    print("Waiting for a rematch request.")
    rematch_request = s.recv(1024)
    rematch_request = pickle.loads(rematch_request)
    rematch_response = "N"

    if rematch_request == "Y":
        print("\nThe other player wants to play again!")
        rematch_response = input("Would you like to rematch? Enter Y or N: ")
        rematch_response = rematch_response.capitalize()
        save_response = rematch_response #cause it is gonna get dumped

        rematch_response = pickle.dumps(rematch_response)
        s.send(rematch_response)

        if save_response == "Y":
            print("Play Again")
            o_player.resetGameBoard()
        else:
            play_again = False

    else:
        print("The other player does not want to play again.")
        play_again = False

print("\nFun Times")
o_player.printStats()            
s.close()
