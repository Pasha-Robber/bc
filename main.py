import cmd

from Blockchain import Blockchain
from Transaction import Transaction

class CLI(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = ' > '
        self.intro = 'Добро пожаловать\nДля справки наберите "help"\n'+'='*50
        self.doc_header = 'Доступные команды (для справки по конкретной команде наберите "help _команда_")'
    
    def default(self, line):
        print('Несуществующая команда')

    def emptyline(self):
        pass

    def do_exit(self, line):
        print('Завершение сеанса...')
        return KeyboardInterrupt

    def do_createBc(self, args):
        bc = Blockchain()
        bc.createBC(args)

    def do_getBalance(self, args):
        """ ---> getBalance -a [address] - получает баланс [address] <--- """
        bc = Blockchain()
        args = args.split(' ')
        if len(args) == 2:
            UTXOs = bc.findUTXO(args[1])
            balance = 0
            for out in UTXOs:
                balance += out['Value']
            print('Баланс {0}: {1}'.format(args[1], balance))
        else:
            print('Нехватает аргументов!')
    
    def do_send(self, args):
        args = args.split(' ')
        bc = Blockchain()
        tx = Transaction()
        if int(args[2]) > 0:
            if tx.newUTXOTransaction(args[0], args[1], int(args[2]), bc):
                bc.addBlock(tx)
                print('Успешно!')
            else:
                print('Недостаточно монет!')
        else:
            print('Введено недопустимое число!')

    def do_printChain(self, args):
        """ ---> printChain - Вывовыводит всю цепь блоков <--- """
        bc = Blockchain()
        bc.printChain()


if __name__ == "__main__":
    cli = CLI()
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print('Завершение сеанса...')