from client import utils
from client.app import App
from client.core import Client

from modules.system import System


HOST: str = '192.168.1.10'
PORT: int = 19000

client = Client(HOST, PORT)


def home(message: str = None):
    System.clear()
    App.home()
    utils.displayMessage(message)

    select = input(" Select: ")
    if select.isdigit():
        option = int(select)
        actions = {
            0: lambda: System.exit(),
            1: lambda: register(),
            2: lambda: login(),
		}
        if option in actions:
            actions[option]()
        else: 
            home("Lựa chọn không hợp lệ.")
    else: 
        home("Vui lòng nhập số.")


def register(message: str = None, username: str = None):
    try:
        System.clear()
        App.register()
        utils.displayMessage(message)

        if username: print("{}Username: {}".format(' ', username))

        if not client.serverConnect():
            client.closeConnection()
            home("Không thể kết nối tới máy chủ!")

        password = None

        # Yêu cầu nhập username cho đến khi người dùng cung cấp giá trị hợp lệ
        while username is None or username.strip() == "":
            username = input("{}Username: ".format(' '))
            if username.strip() == "":
                register("Username không thể để trống.")
            elif username == "0": return home()
            elif len(username) > 16:
                register("Username không thể vượt quá 16 ký tự.")

        # Yêu cầu nhập password cho đến khi người dùng cung cấp giá trị hợp lệ
        while password is None or password.strip() == "":
            password = input("{}Password: ".format(' '))
            if password.strip() == "":
                register("Password không thể để trống.", username)
        
        response = client.submitData('0|{}|{}'.format(username, password))
        return home(response['msg'])
    except Exception as error: 
        register(error)
    finally: 
        client.closeConnection()


def login(message: str = None, username: str = None):
    try:
        System.clear()
        App.login()
        utils.displayMessage(message)

        if not client.serverConnect():
            home("Không thể kết nối tới máy chủ !")
        
        password = None
        
        while username is None or username.strip() == "":
            username = input("{}Username: ".format(' '))
            if username.strip() == "":
                login("Username không thể để trống.")
            elif username == "0": return home()
        
        while password is None or password.strip() == "":
            password = input("{}Password: ".format(' '))
            if password.strip() == "":
                login("Password không thể để trống.", username)

        reponse = client.submitData('1|{}|{}'.format(username, password))
        if not reponse['status']:
            login(reponse['msg'])
        else:
            menu(reponse)
        
    except Exception as error: 
        login(error)
    finally: 
        client.closeConnection()


def menu(userCredentials, message: str = None):
    try:
        System.clear()
        App.menu()
        utils.displayMessage(message)

        select = input(" Select: ")
        if select.isdigit():
            option = int(select)
            actions = {
                0: lambda: home(),
                1: lambda: spins(userCredentials),
                2: lambda: dice(userCredentials),
            }
            if option in actions:
                actions[option]()
            else: menu("Lựa chọn không hợp lệ.")
        else: menu("Vui lòng nhập số.")
    except Exception as error: 
        menu(userCredentials, error)


def spins(userCredentials: dict, message: str = None):
    try:
        System.clear()
        App.spins()
        utils.displayMessage(message)
        
        if not client.serverConnect():
            menu("Không thể kết nối tới máy chủ!")
        
        userData = client.submitData(
            f'1.5|{userCredentials["username"]}|{userCredentials["password"]}'
        )
        userCoins = userData['coin']
        print(f' Username: {userCredentials["username"]}{" "*4}Xu: {userCoins:,}\n')
        
        selection = input('{}Select: '.format(' '))
        if selection.isdigit():
            selection = int(selection)
            if selection == 0:
                menu(userCredentials)
            if not 1 <= selection <= 2:  
                spins(userCredentials, "Lựa chọn không hợp lệ.")
        else:
            spins(userCredentials, "Vui lòng nhập một số hợp lệ.")

        betAmount = input(' Bet: ')
        if not betAmount.isdigit():
            spins(userCredentials, "Bet không đúng.")

        spinResult = client.submitData(
            f'2|{userCredentials["username"]}|{userCredentials["password"]}|{selection}|{betAmount}'
        )
        
        if not spinResult['status']:
            spins(userCredentials, spinResult['msg'])

        utils.spins(spinResult['number'])
        input(f'{' '*4}{spinResult["msg"]}')
        spins(userCredentials)
    except Exception as error:
        spins(userCredentials, str(error))
    finally: 
        client.closeConnection()



def dice(userCredentials, message = None):
    try:
        System.clear()
        App.dice()
        utils.displayMessage(message)
        
        if not client.serverConnect():
            menu("Không thể kết nối tới máy chủ!")

        userData = client.submitData(
            f'1.5|{userCredentials["username"]}|{userCredentials["password"]}'
        )
        userCoins = userData['coin']
        print(f' Username: {userCredentials["username"]}{" "*4}Xu: {userCoins:,}\n')

        selection = input('{}Select: '.format(' '))
        if selection.isdigit():
            selection = int(selection)
            if selection == 0:
                menu(userCredentials)
            if not 1 <= selection <= 2:  
                spins(userCredentials, "Lựa chọn không hợp lệ.")
        else:
            spins(userCredentials, "Vui lòng nhập một số hợp lệ.")

        betAmount = input(' Bet: ')
        if not betAmount.isdigit():
            spins(userCredentials, "Bet không đúng.")

        diceResult = client.submitData(
            f'3|{userCredentials["username"]}|{userCredentials["password"]}|{selection}|{betAmount}'
        )
        
        if not diceResult['status']:
            dice(userCredentials, diceResult['msg'])

        utils.dice(diceResult['number'][-1])
        print(f'{' '*4}Tổng: {diceResult['number'][0]}')
        input(f'{' '*4}{diceResult["msg"]}')
    except Exception as error: return error