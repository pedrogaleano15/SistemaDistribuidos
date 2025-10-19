from Pyro5.api import Proxy, locate_ns

ns= locate_ns(host="172.31.15.125")
uri= ns.lookup("calculadora")
calc= Proxy(uri)
with Proxy(uri) as calc:#cria a referencia a objeto remoto
    print("3 + 4 =", calc.add(3,4))
    print("3 - 4 =", calc.sub(3,4))
    print("3 * 4 =", calc.mul(3,4))
    print("3 / 4 =", calc.div(3,4))