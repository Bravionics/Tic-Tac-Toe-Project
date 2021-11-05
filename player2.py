import socket
import pickle # sending objects

from gameboard import BoardClass


# user asked to provide host information
IP_address = input("Please enter a host IP Address: ")
port = int(input("Please enter a host port: "))

# use that info to establish a server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((IP_address, port))
s.listen(5)

client_socket, client_address = s.accept()
print("\nConnected!")

# wait for player1 to send their username
player1_name = client_socket.recv(1024)
player1_name = player1_name.decode()

# return with player2 username
user_name = input("Please enter your username: ")
client_socket.send(user_name.encode())

x_player = BoardClass("O", user_name, " ")

play_again = True

while play_again == True:
    x_player.updateGamesPlayed()

    x_player.print_board()
    print("\nWaiting for a player to make a move.")
    o_board = client_socket.recv(1024)
    o_board = pickle.loads(o_board)
    x_player.updateGameBoard(o_board)

    while x_player.isWinner("O") == False and x_player.isWinner("X") == False and x_player.boardIsFull() == False:
        x_player.print_board()
        keypad = int(input("Enter a number 1-9: "))
        keypad -= 1
        x_player.edit_board(keypad)

        x_player.print_board()

        x_board = pickle.dumps(x_player.board)
        client_socket.send(x_board)

        if x_player.isWinner("O") == True or x_player.boardIsFull() == True:
            x_player.lastTurnName(user_name)
            break

        print("\nWaiting for the other player.")
        o_board = client_socket.recv(1024)
        o_board = pickle.loads(o_board)
        x_player.updateGameBoard(o_board)

        x_player.lastTurnName(player1_name)

    if x_player.isWinner("O") == True:
        x_player.updateWins()
        print("Hooray, you won the game!")
    elif x_player.boardIsFull() == True and x_player.isWinner("X") != True:
        x_player.updateTies()
        print("Aw, it is a draw.")
    else:
        x_player.updateLosses()
        print("Darn, " + player1_name + " won.")

    rematch_response = input("Would you like to play again? Enter Y or N: ")
    rematch_response = rematch_response.capitalize()
    save_response = rematch_response # cause it will get dumped
    player1_response = ""

    rematch_response = pickle.dumps(rematch_response)
    client_socket.send(rematch_response)

    if save_response == "N":
        play_again = False

    else:
        print("Waiting for the other player.")
        player1_response = client_socket.recv(1024)
        player1_response = pickle.loads(player1_response)
 
        if player1_response == "N":
            print("The other player does not want to play again.")
            play_again = False
        else:
            print("Play again")
            x_player.resetGameBoard()

print("\nFun Times")
x_player.printStats()
client_socket.close()
