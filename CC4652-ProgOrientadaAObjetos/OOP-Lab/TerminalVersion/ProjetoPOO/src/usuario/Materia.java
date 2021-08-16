package usuario;
import java.io.Serializable;
import java.util.ArrayList;

/**
 *
 * @author Ibrahim Jamil Orra (22.118.183-7)
 * @author Pedro Domingues (22.218.019-2)
 * @version alpha 1.0.0
 * 
 */

public class Materia implements Serializable {
	
	///////////////
    /* Atributos */
	///////////////
	
    private String nome;
    private Professor coordenador;
    private ArrayList<Professor> professores = new ArrayList<>();
    
    
    ////////////////
    /* Construtor */
    ////////////////
    
    public Materia (String nome_materia, Professor coordenador_materia)
    {
        nome = nome_materia;
        setCoordenador(coordenador_materia);
    }
    
    
    /////////////
    /* Metodos */
    /////////////
    
    /* Set */
    public void setCoordenador (Professor c)
    {
        coordenador = c;
        removeProfessor(c.getNome()); // verifica se o novo coordenador era um professor, se for remove
    }
    
    
    /* Adicao */
    public void addProfessor(Professor p) // adiciona professor na materia
    {
    	if (professores.contains(p)) {
    		System.out.printf("***ERROR: O professor %s ja ministra a materia %s...\n", p.getNome(), nome);
    		return;
    	}
    	professores.add(p);
    }
    
    
    /* Remocao */
    public void removeProfessor(String nomeProfessor)
    {
		for (int i=0;i<professores.size();i++) { // varre a lista de professores
			if (professores.get(i).getNome().equals(nomeProfessor)){
				professores.remove(i);
				return;
			}
    	}
    }
    
    
    /* Verificacao */
    public boolean checkProfessor(Professor p) 
    {
    	return professores.contains(p);
    }
    
    
    /* "Get" */
    public Usuario getCoordenador () 
    {
    	return coordenador;
    }      
    public String getNome () 
    {
        return nome;
    }

    
    /* Impressao */
    public void printProfessores()
    {
    	int i;
    	for(i = 0 ; i<professores.size() ; i++)
    	{
    		System.out.printf("%s /",professores.get(i).getNome());
    	}
    }
}