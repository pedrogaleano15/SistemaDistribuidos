/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Calculadora;

import java.net.MalformedURLException;
import java.rmi.Naming;
import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JOptionPane;

/**
 *
 * @author Edvaldo
 */
public class Cliente {
    public static void main (String[] args){
        Scanner sc = new Scanner(System.in);
        try {
            Registry meuRegistro = LocateRegistry.getRegistry("localhost",1099);
            Calculadora c = null;
            try {
                c = (Calculadora) Naming.lookup("//localhost/Calculadora");
            } catch (NotBoundException ex) {
                Logger.getLogger(Cliente.class.getName()).log(Level.SEVERE, null, ex);
            } catch (MalformedURLException ex) {
                Logger.getLogger(Cliente.class.getName()).log(Level.SEVERE, null, ex);
            }
            
            while(true){
                String menu = JOptionPane.showInputDialog(" 1 - Somar \n 2 - Subtrair\n 3 - Multiplicação\n 4 - Divisão\n");
                switch(menu){
                    case "1":
                        int x = Integer.parseInt(JOptionPane.showInputDialog("A: "));
                        int y = Integer.parseInt(JOptionPane.showInputDialog("B: "));
                        JOptionPane.showMessageDialog(null, "Soma: "+c.soma(x, y));
                        break;
                    case "2":
                        int x1 =Integer.parseInt(JOptionPane.showInputDialog("A: "));
                        int y2 =Integer.parseInt(JOptionPane.showInputDialog("B: "));
                        JOptionPane.showMessageDialog(null,"Subtração: "+c.subt(x1,y2));
                       break;
                    case "3":
                        int x3=Integer.parseInt(JOptionPane.showInputDialog("A: "));
                        int y3=Integer.parseInt(JOptionPane.showInputDialog("B: "));
                        JOptionPane.showMessageDialog(null,"Multiplicação "+c.mult(x3, y3));
                        break;
                    case "4":
                        int x4=Integer.parseInt(JOptionPane.showInputDialog("A: "));
                        int y4=Integer.parseInt(JOptionPane.showInputDialog("B: "));
                        JOptionPane.showMessageDialog(null,"Divisão "+c.divi(x4, y4));
                        break;
                }
            }
        } catch (RemoteException ex) {
            System.out.println("Erro "+ex.getMessage());
        }       
        
    }
    
}
