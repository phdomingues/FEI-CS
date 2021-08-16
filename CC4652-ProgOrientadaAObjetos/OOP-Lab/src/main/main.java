package main;

import usuario.*;

/**
 *
 * @author Pedro Henrique Silva Domingues (22.218.019-2)
 * @version alpha 1.0.0
 */
public class main {
    public static void main(String[] args) {

    	///////////////////////////////////////////
    	/* Configurando e Criando admin / sistema*/
    	///////////////////////////////////////////
    	
    	Admin adm = new Admin("ADM","user123","senha123");
    	adm.setAdm(adm);
    	
    	
    	
    	/////////////////////////////////////
    	/* Realizando cadastros no sistema */
    	/////////////////////////////////////
    	
    	// De Aluno
    	adm.criaAluno("Matheus", "M123", "Mat123");
    	adm.criaAluno("Gustavo", "G123", "Gus123");
    	adm.criaAluno("Pedro", "P123", "Ped123");
    	// De Professor
    	adm.criaProfessor("Guilherme", "Gui123", "Algoritmos321");
    	adm.criaProfessor("Martuchelli", "Martu123", "Conv321");
    	adm.criaProfessor("Reinaldo", "REInaldo123", "Eletrotecnica321");
    	adm.criaProfessor("Pier", "Eletrica123", "BubbleSort");
    	// De Materia
    	adm.criaMateria("Algoritmos", adm.getProfessor("Guilherme"));
    	adm.criaMateria("Circuitos Eletricos", adm.getProfessor("Martuchelli"));
    	adm.criaMateria("Eletrotecnica", adm.getProfessor("Reinaldo"));
    	// Novo professor na materia
    	adm.addProfessorMateria("Pier", "Algoritmos");
    	// Aluno em materia
    	adm.setMateria("Pedro", "Algoritmos");
    	adm.setMateria("Pedro", "Circuitos Eletricos");
    	adm.setMateria("Pedro", "Grafos"); // Grafos ainda nao esta cadastrado, nao vai adicionar
    	
    	
    	
    	/////////////////////
    	/* Simulando Erros */
    	/////////////////////
    	
    	// Dois Alunos iguais
    	adm.criaAluno("João S.", "Joca123", "Senha123");
    	adm.criaAluno("João D.", "Joca123", "Senha123");
    	// Dois Professores iguais
    	adm.criaProfessor("Toninho", "Grafos123", "Grafos321");
    	adm.criaProfessor("Daniel", "Grafos123", "Grafos321");
    	// Duas Materias iguais
    	adm.criaMateria("Grafos", adm.getProfessor("Toninho"));
    	adm.criaMateria("Grafos", adm.getProfessor("Toninho"));

    	// Professor mudando nota
    	System.out.println("--------------------------------------------------------");    	
    	Professor p = adm.getProfessor("Pier");
    	
    	System.out.println("-> Materias que o professor Pier leciona:");
    	p.printMaterias();
    	System.out.println();
    	
    	System.out.println("--> Professor mudando nota que NAO leciona (Pier -> Circuitos -> Pedro = 10.0):");
    	p.setNota("Pedro",p.getNome(), "Circuitos Eletricos", 10.0); // vai continuar -1
    	System.out.println("|--> Materias e notas de Pedro: ");
    	adm.getAluno("Pedro").printMaterias();
    	System.out.println();
    	
    	System.out.println("--> Professor mudando nota que leciona (Pier -> Algoritmos -> Pedro = 10):");
    	p.setNota("Pedro", p.getNome(), "Algoritmos", 10);
    	System.out.println("|--> Materias e notas de Pedro: ");
    	adm.getAluno("Pedro").printMaterias(); // provando que muda direto no sistema e nao apenas em uma copia
    	
    	System.out.println("--------------------------------------------------------");
    	
    	
    	
    	///////////////////////
    	/* Testando exclusao */
    	///////////////////////
    	
    	System.out.println("*** ANTES:");
    	// imprimindo
    	System.out.println("Alunos:");
    	adm.printAlunos();
    	System.out.println();

    	System.out.println("Professores:");
    	adm.printProfessores();
    	System.out.println();

    	System.out.println("Materias:");
    	adm.printMateria();
    	System.out.println();
    	
    	
    	System.out.println("*** DEPOIS:");
    	// removendo
    	adm.removeAluno("Gustavo");
    	adm.removeProfessor("Guilherme");
    	adm.removeMateria("Eletrotecnica");
    	adm.removeMateria("Algoritmos");
    	// imprimindo denovo
    	System.out.println("Alunos:");
    	adm.printAlunos();
    	System.out.println();

    	System.out.println("Professores:");
    	adm.printProfessores();
    	System.out.println();

    	System.out.println("Materias:");
    	adm.printMateria();
    	System.out.println("--------------------------------------------------------");
    	
    	// testando as alteracoes dentro do sistema
    	System.out.println("Provando que a exclusão da materia afetou os alunos e professores tambem:\n-> Materias de Pedro:");
    	adm.getAluno("Pedro").printMaterias();
    	System.out.println("Materias Professor:");
    	adm.getProfessor("Pier").printMaterias();
    	
    	
    }
}
