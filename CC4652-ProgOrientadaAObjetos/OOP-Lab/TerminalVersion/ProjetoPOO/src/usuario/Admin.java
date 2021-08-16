/**
 * @author Pedro Henrique Silva Domingues (22.218.019-2)
 * @version alpha 1.0.0
 * 
 */
package usuario;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

import sis.*;


public class Admin extends Usuario{
    
	///////////////
    /* Atributos */
	///////////////
	
    private Sistema sistem; // Composicao
    
    ////////////////
    /* Construtor */
    ////////////////
    
    public Admin(String n, String l, String s) 
    {
        super(2, n, l, s);
        sistem = new Sistema();
    }
    public Admin(String n, String l, String s, String filePath)
    {
    	super (2,n,l,s);
    	sistem = lerSistema(filePath);
    }

    
    /////////////
    /* Metodos */
    /////////////
    
    /* Criacao */
    public void criaAluno(String nome, String login, String senha)
    {
        Aluno a = new Aluno(nome, login, senha);
        sistem.adicionaAluno(a);
    }
    public void criaMateria(String nome, Professor coordenador)
    {
    	Materia m = new Materia(nome, coordenador);
    	coordenador.cadastrarMateria(m);
    	sistem.adicionaMateria(m);
    }
    public void criaProfessor(String nome, String login, String senha)
    {
        Professor p = new Professor(nome, login, senha);
        sistem.adicionaProfessor(p);
    }

    
    /* Adicao */
    public void addProfessorMateria(String professor, String materia) 
    {
    	Materia m = getMateria(materia); // puxando materia do sistema
    	m.addProfessor( getProfessor(professor) ); // adicionando o professor a materia
    	getProfessor(professor).cadastrarMateria(m);
    	atualizaMateria(m); // atualizando o sistema com a mudan�a feita
    }

    
    /* Get */
    public Aluno getAluno(String aluno)
    {
    	return sistem.getAluno(aluno);
    }
    public Materia getMateria(String materia) {
    	return sistem.getMateria(materia);
    }
    public Professor getProfessor(String prof) {
    	return sistem.getProfessor(prof);
    }
    
    
    /* Remocao */
    public void removeAluno(String nomeAluno)
    {
        sistem.removeAluno(nomeAluno);
    }
    public void removeMateria(String nomeMateria)
    {
    	sistem.removeMateria(nomeMateria);
    }
    public void removeProfessor(String nomeProfessor)
    {
        sistem.removeProfessor(nomeProfessor);
    }
    
    /* Verificacao */
    public boolean checkAluno(String nome)
    {
    	return sistem.checkAluno(nome);
    }    
    public boolean checkMateria(String nome)
    {
        return sistem.checkMateria(nome);
    }
    public boolean checkProfessor(String nome)
    {
    	return sistem.checkProfessor(nome);
    }
    
    
    /* Impressao */
    public void printAlunos()
    {
    	sistem.printAlunos();
    }
    public void printMateria()
    {
    	sistem.printMaterias();
    }
    public void printProfessores()
    {
    	sistem.printProfessores();
    }
    
    
    /* Atualizacao */
    public void atualizaAluno(Aluno a)
    {
    	sistem.replaceAluno(a);
    }
    public void atualizaMateria(Materia m)
    {
    	sistem.replaceMateria(m);
    }
    public void atualizaProfessor(Professor p)
    {
    	sistem.replaceProfessor(p);
    }

    
    /* Salvando */
    public void salvarSistema() {
    	 
        try {
        	
            String caminho = "SistemaPOO.dat";
            FileOutputStream fileOut = new FileOutputStream(caminho);
            ObjectOutputStream objectOut = new ObjectOutputStream(fileOut);
            objectOut.writeObject(sistem);
            objectOut.close();
            System.out.println("The Object  was succesfully written to a file");
 
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
    
    private Sistema lerSistema(String caminho) {
    	 
        try {
 
            FileInputStream fileIn = new FileInputStream(caminho);
            ObjectInputStream objectIn = new ObjectInputStream(fileIn);
 
            Sistema sis = (Sistema) objectIn.readObject();
 
            System.out.println("The Object has been read from the file");
            objectIn.close();
            return sis;
 
        } catch (Exception ex) {
            ex.printStackTrace();
            return null;
        }
    }
    
}
