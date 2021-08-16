/**
 * 
 * @author Pedro Henrique Silva Domingues
 * @version alpha 1.0.0
 */
package sis;

import java.io.Serializable;
import java.util.ArrayList;

import usuario.*;

public class Sistema implements Serializable {	
	
	///////////////
	/* Atributos */
	///////////////
	
	// funcionais:
    private ArrayList<Aluno> alunos = new ArrayList<>(); // todos os alunos cadastrados na faculdade
    private ArrayList<Professor> professores = new ArrayList<>(); // todos os professores cadastrados na faculdade
    private ArrayList<Materia> materias = new ArrayList<>(); // todas as disciplinas ministradas na faculdade
    
    /////////////
    /* Metodos */
    /////////////
    
    /* Adicao */
    public void adicionaAluno(Aluno a)
    {
    	if (checkAluno(a.getLogin())) 
    	{
    		System.out.printf("Aluno, o usuario %s ja esta cadastrado no sistema\n", a.getLogin());
    		return;
    	}
        alunos.add(a);
    }
    public void adicionaMateria(Materia m)
    {
    	if (checkMateria(m.getNome())) 
    	{
    		System.out.printf("Materia %s ja cadastrado no sistema\n", m.getNome());
    		return;
    	}
    	materias.add(m);
    }
    public void adicionaProfessor(Professor p)
    {
    	if (checkProfessor(p.getLogin()))
    	{
    		System.out.printf("Professor, o usuario %s ja esta cadastrado no sistema\n", p.getLogin());
    		return;
    	}
        professores.add(p);
    }


    /* Confirmacao */
    public boolean checkAluno(String user)
    {
    	for (Aluno a : alunos) 
    	{
    		if (a.getLogin().equals(user))
    		{
    			return true;
    		}
    	}
    	return false;
    }
    public boolean checkMateria(String nome)
    {
    	for (Materia m : materias) 
    	{
    		if (m.getNome().equals(nome))
    		{
    			return true;
    		}
    	}
    	return false;
    }
    public boolean checkProfessor(String user)
    {
    	for (Professor p : professores) 
    	{
    		if (p.getLogin().equals(user))
    		{
    			return true;
    		}
    	}
    	return false;    	
    }
    
    
    /* Get */
    public Aluno getAluno(String aluno) 
    {
    	for (Aluno a : alunos) 
    	{
    		if (a.getNome().equals(aluno) || a.getLogin().equals(aluno))
    		{
    			return a;
    		}
    	}
    	return null;
    }
    public Materia getMateria(String materia) 
    {
    	for (Materia m : materias) 
    	{
    		if (m.getNome().equals(materia))
    		{
    			return m;
    		}
    	}
    	return null;
    }
    public Professor getProfessor(String prof) 
    {
    	for (Professor p : professores) 
    	{
    		if (p.getNome().equals(prof) || p.getLogin().equals(prof))
    		{
    			return p;
    		}
    	}
    	return null;
    }    
    

    /* Impressao */
    public void printAlunos()
    {
    	for (Aluno a : alunos) 
    	{
    		System.out.printf("-> Aluno %s - %s - %s\n",a.getNome(),a.getLogin(),a.getSenha());
    	}
    }
    public void printMaterias()
    {
    	for (Materia m : materias) 
    	{
    		System.out.printf("-> Materia %s - %s - ",m.getNome(), m.getCoordenador().getNome());
    		m.printProfessores();
    		System.out.println();
    	}
    }
    public void printProfessores()
    {
    	for (Professor p : professores) 
    	{
    		System.out.printf("-> Professor %s - %s - %s\n",p.getNome(),p.getLogin(),p.getSenha());
    	}
    }
    

    /* Remocao */
    public void removeAluno(String aluno)
    {
        int i;
        for (i=0;i<alunos.size();i++)
        {
            Aluno a2 = alunos.get(i);
            if(a2.getNome().equals(aluno))
            {
                alunos.remove(i);
                return;
            }
        }
    }
    public void removeMateria(String materia)
    {
    	int i;
    	for (i=0;i<materias.size();i++)
    	{
    		Materia m2 = materias.get(i);
    		if(m2.getNome().equals(materia))
    		{
    			materias.remove(i);
    			return;
    		}
    	}
    }    
    public void removeProfessor(String prof)
    {
        int i;
        for (i=0;i<professores.size();i++)
        {
            Professor p2 = professores.get(i);
            if(p2.getNome().equals(prof))
            {
                professores.remove(i);
                return;
            }
        }
    }
    
    
    /* Atualizacao */
    public void replaceAluno(Aluno a)
    {
    	int i;
        for (i=0;i<alunos.size();i++)
        {
            if(alunos.get(i).getLogin().equals(a.getLogin()))
            {
                alunos.set(i, a);
                return;
            }
        }
    }
    public void replaceMateria(Materia m)
    {
    	int i;
        for (i=0;i<materias.size();i++)
        {
            if(materias.get(i).getNome().equals(m.getNome()))
            {
                materias.set(i, m);
                return;
            }
        }
    }
    public void replaceProfessor(Professor p)
    {
    	int i;
        for (i=0;i<professores.size();i++)
        {
            if(professores.get(i).getLogin().equals(p.getLogin()))
            {
                professores.set(i, p);
                return;
            }
        }
    }
    
}
