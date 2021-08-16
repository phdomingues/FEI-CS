package usuario;

import java.util.ArrayList;




// Ibrahim Jamil Orra | RA: 22.118.183-7

public class Professor extends Usuario {
	
	///////////////
	/* Atributos */
	///////////////
	
    private ArrayList <Materia> materias = new ArrayList<>();
    
    
    ////////////////
    /* Construtor */
    ////////////////
    
    public Professor(String n, String l, String s) 
    { 
        super(1, n, l, s);
    }
    
 
    /////////////
    /* Metodos */
    /////////////
    
    /* Set */
    public void cadastrarMateria(Materia materia)
    {
        materias.add(materia);
    }
    

    /* Get */
    public Materia getMateria(String materia)
    {
    	// atualiza a materia com a do sistema
    	for (int i = 0; i < materias.size() ; i++) {
    		if (materias.get(i).getNome().equals(materia))
    		{
    			materias.remove(i);
    			if (getMateriaSistema(materia) == null) { return null; }
    			materias.add( getMateriaSistema(materia) );
    			return materias.get(materias.size()-1); // retorna o ultimo elemento (o que acabou de ser adicionado)
    		}
    	}
    	return null;
    }
    
    
    /* Verificacao */
    public boolean lecionaMateria(String materia)
    {
    	if (getMateria(materia) == null) { return false; }
    	return true;
    }
    
    
    /* Impressao */
    public void printMaterias() 
    {
    	System.out.printf("%s -> ", this.getNome());
    	for (int i = 0; i < materias.size() ; i++) 
    	{
    		// check para ver se a materia ainda existe
    		Materia m = getMateria(materias.get(i).getNome());
    		if (m != null) { System.out.printf("%s / " , materias.get(i).getNome()); }
    		
    	}
    	System.out.println();
    }
    
}
