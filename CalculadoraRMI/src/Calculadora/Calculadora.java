/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Calculadora;

import java.rmi.Remote;
import java.rmi.RemoteException;

/**
 *
 * @author Edvaldo
 */
public interface Calculadora extends Remote {
    public int soma (int a, int b) throws RemoteException;
    public int subt (int a, int b) throws RemoteException; 
    public int mult (int a, int b) throws RemoteException;
    public int divi (int a, int b) throws RemoteException;
}

