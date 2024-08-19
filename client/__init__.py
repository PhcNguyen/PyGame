from client import utils
from client.app import App
from client.core import Client

from modules.style import Colors
from modules.system import System


HOST: str = '192.168.1.10'
PORT: int = 19000

client = Client(HOST, PORT)


def home(title: str = None):
    System.clear()
    App.home()
    if title: 
        print(f'{Colors.red}{' '*5}{title}{Colors.white}')
    select = input("{}Select: ".format(' '))
    if select.isdigit():
        option = int(select)
        actions = {
            0: lambda: System.exit(),
            1: lambda: register(),
            2: lambda: login(),
		}
        if option in actions:
            actions[option]()
        else: home("Lựa chọn không hợp lệ.")
    else: home("Vui lòng nhập số.")


def register(title: str = None, username: str = None):
    try:
        System.clear()
        App.register()
        print(f'{Colors.red}{" "*5}{title}{Colors.white}' if title else '\n')
        if username: print("{}Username: {}".format(' ', username))
        connection = client.serverConnect()
        if not connection:
            client.closeConnection()
            home(connection)

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
        
        reponse = client.submitData('0|{}|{}'.format(username, password))
        return home(reponse['msg'])
    except Exception as error: return register(error)
    finally: client.closeConnection()


def login(title: str = None, username: str = None):
    try:
        System.clear()
        App.login()
        print(f'{Colors.red}{" "*5}{title}{Colors.white}' if title else '\n')
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
        
    except Exception as error: return login(error)
    finally: client.closeConnection()


def menu(reponse, title: str = None):
    try:
        System.clear()
        App.menu()
        print(f'{Colors.red}{" "*5}{title}{Colors.white}' if title else '\n')
        select = input("{}Select: ".format(' '))
        if select.isdigit():
            option = int(select)
            actions = {
                0: lambda: home(),
                1: lambda: spins(reponse),
                2: lambda: dice(reponse),
            }
            if option in actions:
                actions[option]()
            else: menu("Lựa chọn không hợp lệ.")
        else: menu("Vui lòng nhập số.")
    except Exception as error: return menu(reponse, error)


def spins(reponse: dict, title: str = None):
    try:
        System.clear()
        App.spins()
        print(f'{Colors.red}{" "*5}{title}{Colors.white}' if title else '\n')
        if not client.serverConnect():
            home("Không thể kết nối tới máy chủ !")
        
        data = client.submitData('1.5|{}|{}'.format(
            reponse['username'], reponse['password']
            )
        )
        coin = data['coin']
        print(f' Username: {reponse['username']}{' '*4}Xu: {coin:,}\n')
        
        select = input('{}Select: '.format(' '))
        if select.isdigit():
            select = int(select)
            if select == 0: return home()
            if not 1 <= select <= 2:  
                spins(reponse, "Lựa chọn không hợp lệ. Vui lòng 1 or 2.")
        else:   spins(reponse, "Vui lòng nhập một số hợp lệ.")

        bet = input('{}Bet: '.format(' '))
        if not bet.isdigit():
            spins(reponse, "Bet không đúng.")
            
        reponses = client.submitData('2|{}|{}|{}|{}'.format(
            reponse['username'], reponse['password'], select, bet
        ))
        
        utils.spins(reponses['number'])
        print(f'{' '*3}{reponses['msg']}')
        input()
        spins(reponse)
    except Exception as error: spins(reponse, error)
    finally: client.closeConnection()


def dice(reponse):
    try:
        return
    except Exception as error: return error