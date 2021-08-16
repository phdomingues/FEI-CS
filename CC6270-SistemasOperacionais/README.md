# File-Management-System

# Trabalho de CC6270 - Sistemas Operacionais

Sumário:
========

- [Uso](#uso)
- [Grupo](#grupo)
- [Desenvolvimento](#desenvolvimento)
- [Entrega 1](#entrega-1)
- [Entrega 2](#entrega-2)
- [Entrega 3](#entrega-3)
- [Entrega 4](#entrega-4)
- [Entrega 5](#entrega-5)

# Uso
Para rodar o programa, realize os seguintes passos:

### Instalação:

1) Abra um terminal (Ctrl+Alt+t)
2) Clone o projeto: `cd && git clone https://github.com/12pedro07/File-Management-System`
3) Execute o arquivo install: ` cd ~/File-Management-System && chmod +x ./install && source ./install`

### Execução:

Após instalado, você terá uma pasta na raiz do linux nomeada FMS, para rodar o programa execute o seguinte comando: `source ~/FMS/obj/menu`

# Grupo

|  Nome  |  R.A.  |
|  :---: |  :---: |
| Ibrahim Jamil Orra | 22.118.183-7 |
| Matheus Elias Cruz | 22.118.167-0 | 
| Pedro Henrique Silva Domingues  |  22.218.019-2  |
| Renan Martins | 22.118.025-0 |

# Desenvolvimento

Entregas realizadas:

- [x] Entrega 1
- [x] Entrega 2
- [x] Entrega 3
- [x] Entrega 4
- [x] Entrega 5

Organização detalhada dos processos realizados:
https://www.notion.so/Projeto-de-SO-b13890863847466e944f07cd94aa6080

# Entrega 1

__Tema__: Sistema de gerenciamento de arquivos

__Área do conhecimento__: Nosso grupo propõe a criação de uma aplicação desktop para auxiliar usuários linux a fazer gestão de arquivos, tornando o uso e organização diária de algumas tarefas mais agil. 

Entre esta tarefas, pretendemos implementar:

- Um instalador para facilitar a geração dos executaveis e criação da estrutura na qual o nosso sistema irá interagir;
- Uma agenda para shell, na qual o usuário pode gerenciar e salvar seus contatos;
- Um sistema de backup agendado, no qual o usuário pode inserir uma data para o backup e as pastas que deseja salvar;
- Um sistema de organização de imagens auto-organizado, capaz de gerar uma arvore de diretórios e organizar estas imagens segundo a data de geração.

__Sistema Operacional__: Ubuntu

- Paralelo;
- Monousuario e multiusuario;
- Multitarefa; 
- Multiprocessado;
- Opera em lotes (batch).

Porque escolhemos o sistema operacional Ubuntu:

- É open-source e pode ser rodado nos desktops, ou até mesmo na nuvem, estamos estudando na disciplina de sistemas operacionais, que pode facilitar o desenvolvimento do projeto e nas aplicações dos comandos e conceitos vistos em aula.

__Hardware__: 

- Desktop AMD Ryzen 5 3400g 
- Colorful B550m Gaming Pro 
- 16 gb RAM DDR4 
- 1Tb Hard Disk 
- 500wats de potência

# Entrega 2

* _Processo_:

Um processo pode ser qualquer programa em execução que utilizam um certo espaço de memória em que possam ser executados. Uma entidade ativa que carrega atributos como memoria, estado do hardware e um id chamado de PID (Process IDentification), o UID (User IDentification) e também um GID (Group IDentification).
Processos possuem estados, os quais são:

__NEW__ - Está em estado de criação;

__READY__ - Está aguardando para ser direcionado a uma unidade de processamento;

__RUNNING__ - Suas instruções estão sendo executadas;

__WAITING__ - Em aguardo por um evento, como por exemplo uma entrada/saída de dados;

__TERMINATED__ - Sua execução foi finalizada;



* _Thread_:

Threads são fluxos que ocorrem em paralelo dentro de um mesmo processo, cada uma possuindo seu próprio pc (Program Counter) para gerenciar quais instruções devem ser executadas a seguir. Assim como memoria para armazenamento de variáveis e uma pilha de execução para o histórico de execução. Apesar de cada thread possuir seus proprios recursos, ela é iniciada com uma cópia de seu pai.

No nosso projeto, threads foram implementadas para fazer com que em paralelo a agenda, novo terminal seja aberto e a lista de contatos seja exibida. O código para tal pode ser encontrado em arquivo.c, na função nomeada "mostrar_agenda", aproximadamente linha 106.

* _Escalonamento de processo_:

Escalonamento de processos é a um susbsistema do sistema operacional, o qual decida qual processo poderá fazer o uso da cpu em um dado momento. Os algoritmos aplicados a este são responsáveis por todo o gerenciamento desta logistica.

----

Alguns exemplos de algoritmos de gerenciamento de processos são: Algoritmo do barbeiro e Jantar dos filósofos.

- algoritmo do barbeiro
	- Imagine uma barbearia (memória ram)
	- A barbearia recebe clientes (processos)
	- Se não há clientes, o barbeiro adormece 
	- Se a cadeira do barbeiro estiver livre o cliente vai ser atendido
	- O cliente espera pelo barbeiro se houver uma de espera vazia
	- Se não tive onde sentar, o cliente vai embora.

- algoritmo jantar dos filosofos
	- Uma mesa com cinco filósofos
	- Cada filosófo precisa de dois hashis para comer
	- Eles vão precisar compartilhar os hashis
	- Vão precisar considerar os hashis livres para poderem usar


No nosso projeto aplicaremos estes conhecimentos da seguinte forma:
1. Todo código que estiver rodando será um processo, independente de sua funcionalidade.
2. Threads serão utilizadas para gerenciar tarefas em plano de fundo enquanto o usuário permanece podendo utilizar a interface.
3. Não faremos uso direto de Escalonamento de processo, uma vez que o sistema operacional cumprirá todas as necessidades sob este aspecto.

# Entrega 3

Scripts são conjuntos de comandos que serão interpretados e utilizado para a realizaço de tarefas. No caso do linux, utilizamos o bash como interpretador shell.

No nosso projeto, scripts serão aplicados para interagir com o âmbiente do usuário, preparando esta para o uso do programa. Ou seja, compilando e movendo arquivos, gerando estruturas de pastas, etc. Em mais detalhes, alguns exemplos ja implementados são:

- Compilação de todos os códigos de linguagem C que estiverem na pasta src, independente do nome;
- Organização dos executaveis em uma pasta criada com o nome de "obj";
- Criação da estrutura de pastas na qual o usuário ira interagir;
- ...

Dentro do script, utilizamos técnicas aprendidas em aula, como loops (para varrer multiplos arquivos e executar o comando de compilação para cada um deles), criação de pastas, movimentação de arquivos, "echos" para interagir com o terminal indicando mensagens relevantes do processo, variáveis que auxiliam ma gestão e dinamismo do cdigo, etc.

# Entrega 4

O gerenciamento de memória no projeto foi realizado através da linguagem C, com os comandos malloc para requisitar ao sistema operacional um espaço determinado de memória ram e free para liberar a memoria alocada e não causar vazamento de memoria.

### Perguntas:

__1)__ O software desenvolvido funcionará local ou remotamente?

R: O software funcionará localmente, visto que seu objetivo é gerenciar os arquivos de usuário apenas.


__2)__ A leitura das variáveis referentes ao ambiente operacional será feita via input do usuário ou o próprio software fará esta entrada dos dados?

R: A leitura das variáveis do ambiênte operacional será feita inteiramente via o suftware, por meio de scripts shell e código em linguagem C. O usuário será responsável apenas pela interação com a interface.


__3)__ Há atualizações (hardware e software) necessárias que devem ser feitas e monitoradas para que o projeto desenvolvido funcione?

R: Os requisitos para o projeto desenvolvido são:

	1) Sistema operacional linux;
	2) Possuir compilador gcc instalado;
	3) Possuir python3 instalado;

Não se faz necessário nenhum monitoramento durante o uso do software. Também não se faz necessário qualquer hardware especifico para o correto funcionamento do projeto desenvolvido.

__4)__ Há licenças de software que devem ser consideradas?

R: Não há nenhuma licença necessária a ser considerada. O projeto foi totalmente desenvolvido pelos alunos.

### Conceitos:

__1) Páginação:__

A paginação é uma técnica utilizada para implementar a memória virtual, dividindo esta em páginas, que podem, ou não, estar mapeadas à memoria fisica. Cada um dos endereços de memória virtual páginados, será encaminhado para uma parte da cpu chamada MMU (memory management unit, ou, unidade de gerenciamento de memória), responsável por converter o endereço recebido para um endereço real, da memória RAM física. - [Fonte](http://diatinf.ifrn.edu.br/prof/lib/exe/fetch.php?media=user:1379492:sistemas_operacionais:8-memoria-virtual-paginacao.pdf)

__2) Swap:__

A memoria swap é uma parte do HD separada para auxiliar em caso de _overflow_ da memória RAM, ou seja, quando não existe espaço suficiente na memória para realizar as tarefas em execução, assim o sistema operacional utiliza esta parte do HD em forma de arquivo para compensar a falta de RAM. Este arquivo é dependente do sistema operacional, no windows temos no disco C:/ um arquivo oculto chamado pagefile.sys enquanto no linux no lugar de um arquivo, o swap é realizado em uma partição definida durante a instalação do sistema.

# Entrega 5

* _Número de partições_:

Estamos utilizando uma única partição para desenvolvermos a aplicação dentro do sistema operacional Ubuntu.

* _Espaço da aplicação_:

O espaço da aplicação é de 16KB, no entanto, na hora da criação da árvore de diretórios e na incrementação de usuários o espaço pode aumentar.

* _Tecnologia da aplicação_:
- UFS - Unix File System

Esse sistema de arquivos é mais conhecido por utilizar a estrutura de arquivos hierárquica, como uma árvore usada na organização dos arquivos e diretórios, dividido nos seguintes blocos abaixo.
	- Boot blocks: Contém informação que são iniciados separadamente do sistema de arquivos.
	- Super block: Contém informação necessária sobre o sistema de arquivos.
	- Cylinder groups: Tem a função de agirem como uma partição ou mini-partição.

* _Ambiente da aplicação_:

A aplicação utilizará apenas uma única partição, no ambiente operacional Ubuntu, portanto, vai ficar tudo na mesma plataforma.

### Perguntas

__1)__ Como listar os sistemas de arquivos montados?

R: mount -t ext4

Obs: - ext4 é um sistema de arquivos utilizado pelo Linux a partir de 2008


__2)__ Quais são os passos para montar um sistema de arquivos no linux? Faça uso de um ou mais sistemas de arquivos à sua escolha. Sugere-se que o sistema de arquivo escolhido suporte o projeto que desenvolve.

R: 1º Definir o diretório onde será o ponto de montagem `sudo mount /dev/sda7 /mnt/media`

- O linux já declara o tipo de sistema de arquivos automatico.

2º Quando o sistema de arquivos não é reconhecido, adicionar o parâmetro -t no mount.

* Não utilizaremos o comando mount, para a montagem de um sistema de arquivos, pois não achamos necessário montar uma partição, utilizaremos o UFS do linux.

O linux utiliza Ext4, um sistema de arqivos que, segundo a [documentação oficial da distribuição fedora](https://docs.fedoraproject.org/en-US/Fedora/14/html/Storage_Administration_Guide/newfilesys-ext4.html):

_"Ext4 uses extents (as opposed to the traditional block mapping scheme used by ext2 and ext3), which improves performance when using large files and reduces metadata overhead for large files. In addition, ext4 also labels unallocated block groups and inode table sections accordingly, which allows them to be skipped during a file system check. This makes for quicker file system checks, which becomes more beneficial as the file system grows in size."_

__Tradução livre:__ Ext4 utiliza extensões (contrariamente ao esquema de mapeamento de blocks tradicional ustilizado pelo ext2 e ext3), o que melhora a performance quando utilizando arquivos grandes e reduz o _overhead_ de metadados para estes arquivos. Além disto, o ext4 também rotula blocos desalocados e seções de tabela "inode" correspondentes, o que permite a eles serem pulados durante a verificação de arquivos do sistema. Acelerando estas verificações, o que se torna mais benéfico a medida que o tamanho do sistema de arquivos cresce.

__3)__ Como desmontar um sistema de arquivo?

1º Abra o shell

2º Vá no diretório onde é o ponto de montagem 

3º Digite o comando abaixo

`umount /dev/sda4`


__4)__ Uma vez que o mount foram feitos, ele é perdido a cada reinicialização do equipamento?
Não, pois iremos utilizar o agendador de tarefas.

__5)__ Como tornar permanente as montagens de device que vcs criam?
 crontab - agendador de tarefas
A gente utiliza o agendador de tarefas, através do comando crontab no terminal. Para montar os sistemas de arquivos no dia e hora, especificado, tornando persistente a montagem.

