package Calculadora;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

// Esta é a implementação real da interface.
// Ela estende 'UnicastRemoteObject' para poder ser acessada remotamente.
public class rmi extends UnicastRemoteObject implements Calculadora {

    // Construtor padrão (necessário)
    public rmi() throws RemoteException {
        super(); // Chama o construtor da classe pai
    }

    // Implementação dos métodos da interface
    @Override
    public int add(int a, int b) throws RemoteException {
        System.out.println("Servidor: Recebido pedido de adição.");
        return a + b;
    }

    @Override
    public int sub(int a, int b) throws RemoteException {
        System.out.println("Servidor: Recebido pedido de subtração.");
        return a - b;
    }

    @Override
    public int mul(int a, int b) throws RemoteException {
        System.out.println("Servidor: Recebido pedido de multiplicação.");
        return a * b;
    }

    @Override
    public double div(int a, int b) throws RemoteException {
        System.out.println("Servidor: Recebido pedido de divisão.");
        if (b == 0) {
            // Retorna um erro se tentar dividir por zero
            throw new RemoteException("Divisão por zero não é permitida!");
        }
        return (double) a / b;
    }
}