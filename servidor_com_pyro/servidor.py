from Pyro5.api import expose, Daemon, locate_ns

@expose
class calculador:
    def add (self, a, b):
        return a + b
    def sub (self, a, b):
        return a - b
    def mul (self, a, b):
        return a * b
    def div (self, a, b):
        return a / b
    
if __name__ == "__main__":
#registrar o nome do servidor no name server
    with Daemon(host="172.31.15.125") as daemon:#servidor Pyro
        ns= locate_ns(host="172.31.15.125")
        uri= daemon.register(calculador)#registrar o objeto calculador no remoto
        ns.register("calculadora", uri)#faz com que o cliente busque pelo nome "calculadora"
        daemon.requestLoop()#matem o servidor ativo esperando por chamadas