
/*
 *
 * @author Pedro Domingues
 * @RA 22.218.019-2
 */

package usuario;

public class Usuario {
    
	///////////////
    /* Atributos */
	///////////////
	static private Admin sistemAdm;
    private int permissao; // Dita o que o usuario pode ou nao fazer
    private String nome; // Nome do usuario
    private String login; // Login para entrar no sistema
    private String senha; // Senha para entrar no sistema
    
    
    ////////////////
    /* Construtor */
    ////////////////
    
    public Usuario(int p, String n, String l, String s){ // informacoes completas
        setPermissao(p);
        nome = n;
        login = l;
        senha = s;
    }
    
    
    /////////////
    /* Metodos */
    /////////////
    
    /* Set */
    private void setPermissao(int p){
        if (p < 0){
            permissao = 0;
            return;
        } else if (p > 2){
            permissao = 2;
            return;
        }
        permissao = p;
    }
    public void setNome(String n){
    	if (permissao == 2) { nome = n; }
    }
    public void setLogin(String u){
    	if (permissao == 2) { login = u; }
    }
    public void setSenha(String s){
    	if (permissao == 2) { senha = s; }
    }
    public void setAdm(Admin adm) {
    	if (permissao == 2) { sistemAdm = adm; }
    }
    
    
    /* Get */
    public int getPermissao(){
        return permissao;
    }
    public String getNome(){
        return nome;
    }
    public String getLogin(){
        return login;
    }
    public String getSenha(){
        return senha;
    }
    public String getAdm(){
    	return sistemAdm.getNome();
    }
    
    
    /* Contato com ADM */
    public Materia getMateriaSistema(String materia)
    {
    	return sistemAdm.getMateria(materia);
    }
    
    public Aluno getAluno(String a)
    {
    	if (permissao >= 1)
    	{
    		return sistemAdm.getAluno(a);
    	}
    	return null;
    }
    public void setMateria(String aluno, String materia)
    {
    	if (permissao > 0 && sistemAdm.getMateria(materia) != null)
    	{
    		Aluno a = sistemAdm.getAluno(aluno);
    		a.adicionarMateria( getMateriaSistema(materia) );
    		sistemAdm.atualizaAluno(a);
    	}
    }
    
    public void setNota(String aluno, String materia, double nota)
    {
    	if (permissao == 2)
    	{
    		Aluno a = sistemAdm.getAluno(aluno);
    		a.adicionarMedia(materia, nota);
    		sistemAdm.atualizaAluno(a);
    	} 
    	else
    	{
    		System.out.println("***ERROR: Permissao invalida...");
    	}
    }
    // Overload do metodo setNota
    public void setNota(String aluno, String prof, String materia, double nota)
    {
    	if (permissao == 1 && sistemAdm.getProfessor(prof).lecionaMateria(materia) == true)
    	{
    		Aluno a = sistemAdm.getAluno(aluno);
    		a.adicionarMedia(materia, nota);
    		sistemAdm.atualizaAluno(a);
    	}
    }
}