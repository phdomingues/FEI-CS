// Pedro Henrique Silva Domingues R.A.: 22.218.019-2

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <locale.h>

#include <pthread.h>
#include <sys/wait.h>
#include <string.h>

struct contato{
	char Nome[51];
	char Telefone[21];
	char email[31];
	char Cidade[21];
	char Estado[3];
};

struct agenda{
	struct contato contatos[100];
	int num_contatos;
};

char* concat(const char *s1, const char *s2)
{
    char *result = malloc(strlen(s1) + strlen(s2) + 1); // +1 for the null-terminator
    // in real code you would check for errors in malloc here
    strcpy(result, s1);
    strcat(result, s2);
    return result;
}

void trata_gets(char* obj_tratado){
	int i;
	for (i=0;obj_tratado[i]!='\0';i++){
		if (obj_tratado[i] == '\n')
			obj_tratado[i] = '\0';
	}
}

int busca_contato(struct agenda ag, char cont[]){
	int i;
	for (i=0;i<ag.num_contatos;i++){
		if (strcmp(ag.contatos[i].Nome,cont) == 0)
			return i;
	}
	return -1;
}

int i=0;
void* PrintHello(void* ag_){
	struct agenda* ag;
	ag = (struct agenda*)ag_;
	printf("Hello, I recieved: %ld!\n", ag->num_contatos);
	system(concat("echo ", "teste"));
  pthread_exit(NULL);
}

void encontrar_contato(struct agenda ag){

	printf("\n\n-------------------------------------------------------\n\n");

	char encontra[51];
	__fpurge(stdin);
	printf("Por favor digite o nome do contato: ");
	gets(encontra);
	trata_gets(encontra);

	int idx = busca_contato(ag,encontra);

	if (idx >= 0){
		printf("\n---> Informações:\n");
		printf("Nome: %s\n", ag.contatos[idx].Nome);
		printf("Telefone %s\n", ag.contatos[idx].Telefone);
		printf("e-mail: %s\n", ag.contatos[idx].email);
		printf("Cidade: %s\n", ag.contatos[idx].Cidade);
		printf("Estado (2 letras): %s\n", ag.contatos[idx].Estado);
	} else {
		printf("\n\n\t\tERRO: CONTATO INEXISTENTE");
	}

	printf("\n\n-------------------------------------------------------\n\n");

}

void mostrar_agenda(struct agenda ag){

	printf("\n\n-------------------------------------------------------\n\n");

	int i;
	if (ag.num_contatos == 0){
		printf("Agenda Vazia...\n");
		printf("\n\n-------------------------------------------------------\n\n");
		return;
	}

	printf("\n\t*** CONTATOS ***\n\nID   Nome\n\n");
	for (i=0 ; i<ag.num_contatos ; i++){
		printf("%d -> %s\n", i, ag.contatos[i].Nome);
	}
	printf("\n---> Numero total de contatos: %d\n",ag.num_contatos);

	printf("\n\n-------------------------------------------------------\n\n");

}

void inserir_contato(struct agenda* ag){

	printf("\n\n-------------------------------------------------------\n\n");

	struct contato ctt;
	printf("- Por favor insira as informações pedidas:\n");

	// limpando o buffer
	__fpurge(stdin);

	// coletando as informações
	printf("Nome: ");
	fgets(ctt.Nome,51,stdin);
	trata_gets(ctt.Nome);

	__fpurge(stdin);
	printf("Telefone: ");
	fgets(ctt.Telefone,21,stdin);
	trata_gets(ctt.Telefone);

	__fpurge(stdin);
	printf("e-mail: ");
	fgets(ctt.email,31,stdin);
	trata_gets(ctt.email);

	__fpurge(stdin);
	printf("Cidade: ");
	fgets(ctt.Cidade,21,stdin);
	trata_gets(ctt.Cidade);

	__fpurge(stdin);
	printf("Estado (2 letras): ");
	fgets(ctt.Estado,3,stdin);
	trata_gets(ctt.Estado);

	ag->contatos[ag->num_contatos] = ctt;
	ag->num_contatos++;

	printf("\n\n-------------------------------------------------------\n\n");

}

void remover_contato(struct agenda* ag){

	printf("\n\n-------------------------------------------------------\n\n");

	char del[51];
	__fpurge(stdin);
	printf("Por favor digite o nome do contato: ");
	gets(del);
	trata_gets(del);

	int idx = busca_contato(*ag,del);
	if (idx >= 0){
		ag->contatos[idx] = ag->contatos[(ag->num_contatos)-1];
		ag->num_contatos -= 1;
		printf("\nContato excluido com sucesso!\n");
	} else {
		printf("\n\t\tERRO: CONTATO INEXISTENTE\n");
	}

	printf("\n\n-------------------------------------------------------\n\n");

}

void alterar_contato(struct agenda* ag){

	printf("\n\n-------------------------------------------------------\n\n");

	char* cont = malloc(51*sizeof(char));

	__fpurge(stdin);
	printf("Por favor digite o nome do contato: ");
	gets(cont);
	trata_gets(cont);

	int idx = busca_contato(*ag,cont);
	free(cont);

	if (idx<0){
		printf("\n\n\t\tERRO: CONTATO INEXISTENTE\n");
		printf("\n\n-------------------------------------------------------\n\n");
		return;
	} else {
		// muda a referencia de ultimo contato para fazer a mudança e depois volta a posição correta
		int backup = ag->num_contatos;
		ag->num_contatos = idx;
		inserir_contato(ag);
		ag->num_contatos = backup;
		printf("\nContato modificado com sucesso\n");
		printf("\n\n-------------------------------------------------------\n\n");
	}

}

void salvar_txt(struct agenda ag){
	int i;
	FILE* arq = fopen("agenda.txt","w");

	for (i=0;i<ag.num_contatos;i++){
		fprintf(arq, "Nome: %s\n",					ag.contatos[i].Nome			);
		fprintf(arq, "Telefone: %s\n",			ag.contatos[i].Telefone	);
		fprintf(arq, "e-mail: %s\n",				ag.contatos[i].email		);
		fprintf(arq, "Cidade: %s\n",				ag.contatos[i].Cidade		);
		fprintf(arq, "Estado: %s\n\n",			ag.contatos[i].Estado		);
	}
	fclose(arq);
}

struct agenda carrega_agenda_txt(){
	int i,item=0,gravar = 0;
	char info[200];
	char aux[2];

	// construindo agenda
	struct agenda ag;
	ag.num_contatos = 0;

	FILE* arq = fopen("agenda.txt","r");
	char ch_at, ch_ant;


	// rodando por todo o arquivo
	while ( (ch_at=fgetc(arq)) != EOF ){

		// se encontrar ": "
		if (ch_ant==':' && ch_at==' '){ gravar = 1;	}

		// se terminar a linha
		if (ch_at == '\n'){
			gravar = 0; // para de gravar ate encontrar ": " novamente

			// se rodou por todos os itens da agenda para um contato
			if (item >= 10){ // muda o contato
				item = 0;
			} else { // senao, ir para o proximo item da agenda

				// shift para esquerda para arrumar o vetor
				for (i=1;info[i]!='\0';i++) { info[i-1] = info[i]; }
				info[i-1] = '\0';

				switch(item){
					case 0:
						strcpy(ag.contatos[ag.num_contatos].Nome,info);
					break;

					case 1:
						strcpy(ag.contatos[ag.num_contatos].Telefone,info);
					break;

					case 2:
						strcpy(ag.contatos[ag.num_contatos].email,info);
					break;

					case 3:
						strcpy(ag.contatos[ag.num_contatos].Cidade,info);
					break;

					case 4:
						strcpy(ag.contatos[ag.num_contatos].Estado,info);
						ag.num_contatos++;
					break;

					default:
						printf("INTERNAL ERROR 001");

				}
				item++; // item = item da agenda

			}
			info[0] = '\0';
		}

		// se estiver no momento de gravar
		if (gravar == 1){
			// cria um vetor com todas as informações coletadas para 1 contato
			aux[0] = ch_at;
			strcat(info,aux);
		}

		ch_ant = ch_at;
	}

	fclose(arq);
	return ag;
}

struct agenda carrega_agenda_bin(){
	int i, tamanho;

	// ponteiro para o arquivo
	FILE* arq_bin = fopen("agenda.bin","rb");

	// check para saber se o arquivo existe
	if (arq_bin == NULL){
		printf("\tERROR: ARQUIVO INEXISTENTE\n\n");
		struct agenda a;
		return a;
	}

	// aloca espaço para carregar o arquivo
	struct agenda* ag = malloc(sizeof(struct agenda));

	// le o arquivo
	fread(ag,sizeof(struct agenda),1,arq_bin);

	// usa uma agenda auxiliar para liberar o espaço alocado
	struct agenda aux = *ag;
	free(ag);

	return aux;
}

void salvar_bin(struct agenda ag){
	FILE* arq_bin = fopen("agenda.bin","wb");

	fwrite(&ag, sizeof(struct agenda), 1, arq_bin); // gravando a agenda

	fclose(arq_bin);
}

int main(int argc, char* argv[]){
	int option, sair = 0;

	// habilitando teclas pt-br
	setlocale(LC_ALL, "Portuguese");

	// carregando a agenda ou criando nova
	printf("Carregar arquivo binário (0) / Carregar arquivo de texto (1) / Criar uma nova agenda (2): ");
	scanf("%d",&option);
	struct agenda ag;
	if (option == 0){
		ag = carrega_agenda_bin();
		mostrar_agenda(ag);
	} else if (option == 1) {
		ag = carrega_agenda_txt();
		mostrar_agenda(ag);
	} else  if (option == 2){
		// cria agenda:
		ag.num_contatos = 0;
		system("clear");
	} else {
		printf("\n\tERROR: CÓDIGO INVALIDO\n\n\tFECHANDO AGENDA\n\n");
		sair = 1;
	}

	// main loop
	while (sair == 0){

 		printf("               _____ ______ _   _ _____           \n");
		printf("         /\\   / ____|  ____| \\ | |  __ \\   /\\     \n");
		printf("        /  \\ | |  __| |__  |  \\| | |  | | /  \\    \n");
		printf("       / /\\ \\| | |_ |  __| | . ` | |  | |/ /\\ \\   \n");
		printf("      / ____ \\ |__| | |____| |\\  | |__| / ____ \\  \n");
		printf("     /_/    \\_\\_____|______|_| \\_|_____/_/    \\_\\ \n\n");
		printf("\t(1) -> Adicionar Contato;\n");
		printf("\t(2) -> Remover Contato;\n");
		printf("\t(3) -> Imprimir todos os Contatos;\n");
		printf("\t(4) -> Informações de Contato;\n");
		printf("\t(5) -> Modificar informações de Contato;\n");
		printf("\t(6) -> Salvar agenda em formato txt;\n");
		printf("\t(7) -> Salvar agenda em formado binário;\n");
		printf("\t(8) -> Sair;\n");
		printf(">>> ");
		scanf("%d",&option);
		puts("");
		system("clear");

		pthread_t thread;
		int rc;
		switch(option)
		{
			case 1 :
				inserir_contato(&ag);
			break;

			case 2:
				remover_contato(&ag);
			break;

			case 3:
				// printf("In main: creating thread\n");
				// rc = pthread_create(&thread, NULL, PrintHello, (void*)&ag);
				// i++;
				// if (rc){
				// 	printf("ERROR; return code from pthread_create() is %d\n", rc);
				// 	exit(-1);
				// }
				//system("gnome-terminal -e command");
				mostrar_agenda(ag);
			break;

			case 4:
				encontrar_contato(ag);

			break;

			case 5:
				alterar_contato(&ag);
			break;

			case 6:
				salvar_txt(ag);
			break;

			case 7:
				salvar_bin(ag);
			break;

			case 8:
				printf("Saindo...\n\n");
				sair = 1;
			break;

			default:
				printf("\t\t\n\nERROR: CÓDIGO INVALIDO...\n\n");
		}
		system("clear");
	}

	pthread_exit(NULL);
	return 0;
}
