/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package usuario;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 *
 * @author unifmguedes
 */
public class Aluno extends Usuario
{
	
    ///////////////
    /* Atributos */
    ///////////////
	
    private HashMap<Materia,Double> materiasENotas; // keys = Objetos materia / values = Double
    
    
    ////////////////
    /* Construtor */
    ////////////////
    
    public Aluno(String n, String l, String s) 
    {
        super(0, n, l, s);
        materiasENotas = new HashMap<>();
    }
    
    
    /////////////
    /* Metodos */
    /////////////
    
    /* Adicao */
    public void adicionarMateria(Materia m) // Materias novas sao criadas com media = -1 para controle
    {
    	if (materiasENotas.containsKey(m))
    	{ 
    		System.out.printf("***ERROR: O aluno %s ja cursa a materia *s...\n",this.getNome(),m.getNome());
    		return;
    	}
        materiasENotas.put(m, -1.0);
    }
    public void adicionarMedia(String nomeMateria, double nota)
    {
    	// encontra a materia
    	for (Map.Entry<Materia,Double> m : materiasENotas.entrySet())
    	{
    		if (m.getKey().getNome().equals(nomeMateria))
    		{
    			// garante nota entre 0 e 10
    			nota = (nota > 10) ? 10 : nota;
    			nota = (nota <  0) ?  0 : nota;
    			// substitui a nota atual do aluno
    			materiasENotas.put(m.getKey(), nota);
    			atualizaMateria(m.getKey());
    			return;
    		}
    	}
    }
    
    
    /* Atualizacao */
    private void atualizaMateria(Materia m)
    {
    	try {
    	// setup
    	double nota = materiasENotas.get(m);
    	String nomeMateria = m.getNome();
    	Materia materia = getMateriaSistema(nomeMateria); // puxa a materia atualizada do sistema
    	// exclusao
    	materiasENotas.remove(m); // remove a materia antiga
    	// replace apenas se a materia ainda existe no sistema
    	if (materia != null) { materiasENotas.put(materia, nota); }// atualiza o hashmap com a materia nova, preservando a nota 
    	}	
    	catch (NullPointerException excpt) {}
    }
    
    
    /* Get */
    public Materia getMateria(String nomeMateria)
    {
    	for (Map.Entry<Materia,Double> m : materiasENotas.entrySet())
    	{
    		if (m.getKey().getNome().equals(nomeMateria))
    		{
    			atualizaMateria(m.getKey());
    			return m.getKey();
    		}
    	}
    	return null;
    }
    
    
    /* Impressao */
    public void printMaterias() // Metodo auxiliar para visualizacao 
    {
    	ArrayList<Materia> aux = new ArrayList<>();
    	// atualizando as materias (meio gambiarra, melhorar depois)
    	for (Map.Entry<Materia,Double> m : materiasENotas.entrySet()){ aux.add(m.getKey()); }
    	for (Materia matAux : aux) { atualizaMateria(matAux); }
    	
    	// imprimindo
    	for (Map.Entry<Materia,Double> m : materiasENotas.entrySet())
    	{
    		System.out.printf("Materia %s - Media %.2f\n", m.getKey().getNome(),m.getValue());
    	}
    }
    
}
