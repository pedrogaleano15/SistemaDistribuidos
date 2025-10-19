package Calculadora;

import java.rmi.Remote;
import java.rmi.RemoteException;

// Esta é a interface remota.
// Ela precisa estender 'Remote' e todos os métodos devem lançar 'RemoteException'.
public interface Calculadora extends Remote {
    
    // Métodos que o cliente pode chamar (assumindo os nomes)
    public int add(int a, int b) throws RemoteException;
    public int sub(int a, int b) throws RemoteException;
    public int mul(int a, int b) throws RemoteException;
    public double div(int a, int b) throws RemoteException;
}