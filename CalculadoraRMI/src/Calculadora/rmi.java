/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Calculadora;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

/**
 *
 * @author Edvaldo
 */
public class rmi extends UnicastRemoteObject implements Calculadora{
    public rmi () throws RemoteException{
        int a,b;
    }
    public int soma (int a, int b) throws RemoteException{
        return a+b;
    }
    public int subt(int a, int b) throws RemoteException{
        return a - b;
    }
    public int mult(int a, int b) throws RemoteException{
        return a * b;
    }
    public int divi(int a, int b) throws RemoteException{
        if(b==0)
            return 0;
        else
            return a/b;
    }
}
