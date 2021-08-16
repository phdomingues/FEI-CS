package main;

import java.util.Scanner;
import usuario.*;

/**
 *
 * @author Pedro Henrique Silva Domingues (22.218.019-2)
 * @version alpha 1.0.0
 */
public class main {
    
    public static Aluno loginAluno(Admin adm){
        Scanner input = new Scanner(System.in);
        Aluno user;
        String login;
        String senha;
        System.out.print("Login: ");
        login = input.nextLine();
        System.out.print("Senha: ");
        senha = input.nextLine();
        if (adm.getAluno(login) == null){
            System.out.println("Usuario não cadastrado no sistema");
            return null;
        }
        else{ 
            user = adm.getAluno(login);
            if (senha.equals(user.getSenha())){
                return user;
            }
        System.out.println("senha invalida");
        return null;
        }
    }
    
        public static Professor loginProf(Admin adm){
        Scanner input = new Scanner(System.in);
        Professor user;
        String login;
        String senha;
        System.out.print("Login: ");
        login = input.nextLine();
        System.out.print("Senha: ");
        senha = input.nextLine();        
        if (adm.getProfessor(login) == null){
            System.out.println("Usuario não cadastrado no sistema");
            return null;
        }
        else{
            user = adm.getProfessor(login);
            System.out.println(user.getNome());
            System.out.println(user.getSenha());
            if (senha.equals(user.getSenha())){
                return user;
            }
        System.out.println("senha invalida");
        return null;
        }
    }
    
    public static void main(String[] args) {

    	///////////////////////////////////////////
    	/* Configurando e Criando admin / sistema*/
    	///////////////////////////////////////////
    	
//    	Admin adm = new Admin("adm", "adm", "adm");;
//   	adm.setAdm(adm);
    	
    	Admin adm = new Admin("adm", "adm", "adm","SistemaPOO.dat");
        

//        adm.criaAluno("pedro", "uniepedomingues", "senha");
//        adm.criaAluno("greg", "uniegreg", "senha");
//
//        adm.criaProfessor("Toninho", "LoveGrafos", "GrafosLove");
//        adm.criaProfessor("Danilo", "POO", "POO123");
//        adm.criaProfessor("Leandro", "LABPOO", "LAB123");
//        
//        adm.criaMateria("Grafos", adm.getProfessor("Toninho"));

        System.out.println(" >>>> Debug tools: \n"
                + "Materias:");
        adm.printMateria();
        System.out.println("\nProfessores: ");
        adm.printProfessores();
        System.out.println("\nAlunos: ");
        adm.printAlunos();
        Aluno a = null;
        Professor p = null;
        boolean flag = false;
    	
    	///////////////
    	/* Funcional */
    	///////////////
        
        Scanner input = new Scanner(System.in);
        System.out.print("Aluno (a) / Professor (p) / adm (d): ");
        String type = input.nextLine();
        
        if (type.equals("a")){
            while(!flag){
                a = loginAluno(adm);
                if (a != null)
                    flag = true;
            }
            
            // Janela do aluno
            flag = false;
            while(!flag){
                System.out.print("Escolha uma opção:\n"
                        + "m [materias e professores]\n"
                        + "p [verificar professores de uma materia]\n"
                        + "s [sair]\n"
                        + "\n>>> ");
                
                String option = input.nextLine();
                
                System.out.println("\n------------------------------------------");
                switch(option){
                    case "m":
                        System.out.println(">>> Materias <<<");
                        a.printMaterias();
                        System.out.println("\n------------------------------------------");
                        break;
                    case "n":
                        System.out.print("Materia: ");
                        String inputMat = input.nextLine();
                        Materia tryMateria = a.getMateria(inputMat);
                        if (tryMateria != null){
                            tryMateria.printProfessores();
                        }
                        break;
                    case "s":
                        System.out.println("Saindo...");
                        flag = true;
                        break;
                }
                
                System.out.println("\n");
                
            }
            
        } else if (type.equals("p")){
            while(!flag){
                p = loginProf(adm);
                if (p != null)
                    flag = true;
            }
            
            
            // Janela do professor
            flag = false;
            while(!flag){
                System.out.print("Escolha uma opção:\n"
                        + "m [materias ministradas]\n"
                        + "c [cadastrar aluno em materia]\n"
                        + "s [sair]\n"
                        + "\n>>> ");
                
                String option = input.nextLine();
                
                System.out.println("\n------------------------------------------");
                switch(option){
                    case "m":
                        System.out.println(">>> Materias <<<");
                        p.printMaterias();
                        System.out.println("\n------------------------------------------");
                        break;
                    case "c":
                        System.out.print("Materia: ");
                        String nomeMat = input.nextLine();
                        Materia tryMateria = p.getMateria(nomeMat);
                        if (tryMateria != null){
                            System.out.print("Nome do aluno: ");
                            String nomeAlun = input.nextLine();
                            Aluno alun = adm.getAluno(nomeAlun);
                            if (alun != null){
                                adm.setMateria(nomeAlun, nomeMat);
                            }
                        }
                        break;
                    case "s":
                        System.out.println("Saindo...");
                        flag = true;
                        adm.salvarSistema();
                        break;
                }
                
                System.out.println("\n");
                
                
            }
        } else if (type.equals("d")){
            String name;
            String log;
            String sen;
            // Janela do professor
            flag = false;
            while(!flag){
                System.out.print("Escolha uma opção:\n"
                            + "a [cadastrar aluno]\n"
                            + "p [cadastrar professor]\n"
                            + "m [cadastrar materia]\n"
                            + "ea [excluir aluno]\n"
                            + "ep [excluir professor]\n"
                            + "em [excluir materia]\n"
                            + "s [salvar e sair]\n"
                            + "\n>>> ");

                    String option = input.nextLine();

                    System.out.println("\n------------------------------------------");

                    switch(option){
                        case "a":
                            System.out.println(">>> nome: ");
                            name = input.nextLine();
                            System.out.println(">>> login: ");
                            log = input.nextLine();
                            System.out.println(">>> senha: ");
                            sen = input.nextLine();

                            adm.criaAluno(name, log, sen);
                            break;
                        case "p":
                            System.out.println(">>> nome: ");
                            name = input.nextLine();
                            System.out.println(">>> login: ");
                            log = input.nextLine();
                            System.out.println(">>> senha: ");
                            sen = input.nextLine();

                            adm.criaProfessor(name, log, sen);
                            break;
                        case "m":
                            System.out.println(">>> nome: ");
                            name = input.nextLine();
                            System.out.println(">>> LISTA DE PROFESSORES <<<: ");
                            adm.printProfessores();
                            System.out.println();
                            System.out.println(">>> coordenador: ");
                            String prof = input.nextLine();
                            adm.criaMateria(name, adm.getProfessor(prof));
                            break;
                        case "em":
                            adm.printMateria();
                            System.out.println(">>> nome materia: ");
                            name = input.nextLine();
                            adm.removeMateria(name);
                            break;
                        case "ea":
                            adm.printAlunos();
                            System.out.println(">>> nome: ");
                            name = input.nextLine();
                            adm.removeAluno(name);
                            break;
                        case "ep":
                            adm.printProfessores();
                            System.out.println(">>> nome: ");
                            name = input.nextLine();
                            adm.removeProfessor(name);
                            break;
                        case "s":
                            System.out.println("Saindo...");
                            flag = true;
                            adm.salvarSistema();
                            break;
                    }
                }
            }
        
        
        
        
    	////////////// <<<<<<<<<<<<<<<<<<<<
    	/* TESTES */// <<<<<<<<<<<<<<<<<<<<
    	////////////// <<<<<<<<<<<<<<<<<<<<

        
    	/////////////////////////////////////
    	/* Realizando cadastros no sistema */
    	/////////////////////////////////////
    	
//    	// De Aluno  ("NOME",    "USER", "SENHA")
//    	adm.criaAluno("Matheus", "M123", "Mat123");
//    	adm.criaAluno("Gustavo", "G123", "Gus123");
//    	adm.criaAluno("Pedro",   "P123", "Ped123");
//    	// De Professor  ("NOME",        "USUARIO",      "SENHA")
//    	adm.criaProfessor("Guilherme",   "Gui123",      "Algoritmos321");
//    	adm.criaProfessor("Martuchelli", "Martu123",    "Conv321");
//    	adm.criaProfessor("Reinaldo",    "REInaldo123", "Eletrotecnica321");
//    	adm.criaProfessor("Pier",        "Eletrica123", "BubbleSort");
//    	// De Materia  ("NOME",     Professor coordenador);       
//    	adm.criaMateria("Algoritmos", adm.getProfessor("Guilherme"));
//    	adm.criaMateria("Circuitos Eletricos", adm.getProfessor("Martuchelli"));
//    	adm.criaMateria("Eletrotecnica", adm.getProfessor("Reinaldo"));
//    	// Novo professor na materia
//    	adm.addProfessorMateria("Pier", "Algoritmos");
//    	// Aluno em materia
//    	adm.setMateria("Pedro", "Algoritmos");
//    	adm.setMateria("Pedro", "Circuitos Eletricos");
//    	adm.setMateria("Pedro", "Grafos"); // Grafos ainda nao esta cadastrado, nao vai adicionar
//    	
//    	
//    	
//    	/////////////////////
//    	/* Simulando Erros */
//    	/////////////////////
//    	
//    	// Dois Alunos iguais
//    	adm.criaAluno("Joao S.", "Joca123", "Senha123");
//    	adm.criaAluno("Joao D.", "Joca123", "Senha123");
//    	// Dois Professores iguais
//    	adm.criaProfessor("Toninho", "Grafos123", "Grafos321");
//    	adm.criaProfessor("Daniel", "Grafos123", "Grafos321");
//    	// Duas Materias iguais
//    	adm.criaMateria("Grafos", adm.getProfessor("Toninho"));
//    	adm.criaMateria("Grafos", adm.getProfessor("Toninho"));
//
//    	// Professor mudando nota
//    	System.out.println("--------------------------------------------------------");    	
//    	Professor p = adm.getProfessor("Pier");
//    	
//    	System.out.println("-> Materias que o professor Pier leciona:");
//    	p.printMaterias();
//    	System.out.println();
//    	
//    	System.out.println("--> Professor mudando nota que NAO leciona (Pier -> Circuitos -> Pedro = 10.0):");
//    	p.setNota("Pedro",p.getNome(), "Circuitos Eletricos", 10.0); // vai continuar -1
//    	System.out.println("|--> Materias e notas de Pedro: ");
//    	adm.getAluno("Pedro").printMaterias();
//    	System.out.println();
//    	
//    	System.out.println("--> Professor mudando nota que leciona (Pier -> Algoritmos -> Pedro = 10):");
//    	p.setNota("Pedro", p.getNome(), "Algoritmos", 10);
//    	System.out.println("|--> Materias e notas de Pedro: ");
//    	adm.getAluno("Pedro").printMaterias(); // provando que muda direto no sistema e nao apenas em uma copia
//    	
//    	System.out.println("--------------------------------------------------------");
//    	
//    	
//    	
//    	///////////////////////
//    	/* Testando exclusao */
//    	///////////////////////
//    	
//    	System.out.println("*** ANTES:");
//    	// imprimindo
//    	System.out.println("Alunos:");
//    	adm.printAlunos();
//    	System.out.println();
//
//    	System.out.println("Professores:");
//    	adm.printProfessores();
//    	System.out.println();
//
//    	System.out.println("Materias:");
//    	adm.printMateria();
//    	System.out.println();
//    	
//    	
//    	System.out.println("*** DEPOIS:");
//    	// removendo
//    	adm.removeAluno("Gustavo");
//    	adm.removeProfessor("Guilherme");
//    	adm.removeMateria("Eletrotecnica");
//    	adm.removeMateria("Algoritmos");
//    	// imprimindo denovo
//    	System.out.println("Alunos:");
//    	adm.printAlunos();
//    	System.out.println();
//
//    	System.out.println("Professores:");
//    	adm.printProfessores();
//    	System.out.println();
//
//    	System.out.println("Materias:");
//    	adm.printMateria();
//    	System.out.println("--------------------------------------------------------");
//    	
//    	// testando as alteracoes dentro do sistema
//    	System.out.println("Provando que a exclus�o da materia afetou os alunos e professores tambem:\n-> Materias de Pedro:");
//    	adm.getAluno("Pedro").printMaterias();
//    	System.out.println("Materias Professor:");
//    	adm.getProfessor("Pier").printMaterias();
//    	
//    	adm.salvarSistema();
//    	
    }
}