---
title: Como fazer um LEITOR de texto
tag: C
date: jun 2026
---

# Era pra ser um editor de texto baseado em VIM.

## Introdução:

Estava caçando projetos pra melhorar minha lógica. Nada melhor do que pausar JAVA e ir pra C. (meu cérebro deve me odiar).

## 1. Como eu começaria arquitetando um editor de texto?

Hmmmmmmmmmmmm, primeiro, eu comecei tentando descobrir como ler um arquivo e printar o conteúdo dele no terminal.

minto, comecei aprendendo oque VIM faz que é limpar a tela e printar o conteúdo na tela.

```c
#include <stdio.h>

void clearScreen() {
    printf("\033[H\033[J");
}

int main(void) {
    clearScreen();
    printf("hello from C\n");
    return 0;
}
```

```c
printf("\033[H\033[J");
```

Aqui, eu descobri que o terminal pode interpretar ASCII, e esse comando basicamente,limpa o terminal e joga o cursor pra cima e na esquerda.

ééééééééééé.... huuuuuu,

depois, ai sim, eu fui pra descobrir como ler o conteúdo de um arquivo e printar o conteúdo no terminal

```c
    FILE *file_ptr;
    
    file_ptr = fopen("teste.txt", "r");

    if (file_ptr == NULL) {
        printf("Error: não deu pra achar arquivo.\n");
        return 1;
    }

    clearScreen();

    char buffer[256];

    while (fgets(buffer, sizeof(buffer), file_ptr) != NULL) {
        printf("%s", buffer);
    }

    fclose(file_ptr);
```

aqui, eu criei um ponteiro que recebe "FILE *", basicamente, é um espaço na memória capaz de ALOCAR o endereço pra um arquivo existente, não o conteúdo do arquivo, mas o endereço do arquivo.(correção: é um ponteiro pra uma estrutura interna da bibilioteca padrão em C)

depois eu defino o valor do ponteiro como fopen, ou seja, ele abre o arquivo em modo de leitura, se falhar, a função retorna NULL. mas a partir desse momento, eu consigo ler o conteúdo do arquivo.

então, eu crio uma cadeia de caracteres com no maximo 256 caracteres.

```c
    while (fgets(buffer, sizeof(buffer), file_ptr) != NULL) {
```

esse cara ai, é feito pra ler o conteúdo do arquivo linha por linha, o primeiro parâmetro, é onde ele vai alocar os caracteres, nessa primeira versão, nós alocamos cada char da UNICA LINHA de texto que o arquivo possui (se tiver uma quebra de linha, ele não vai ler), o parâmetro "sizeof(buffer)" é pra função não ler mais do que a variável "buffer" é capaz de guardar, no caso, 256 bytes, apontando pro arquivo do que está no ponteiro, se der errado ele vai ser igual a NULL e então, o loop não vai acontecer

depois a gente imprime tudo que o buffer guardou:

```c
    printf("%s", buffer);
```

isso vai imprimir uma única linha, não é muito, mas ja é o suficiente.

nisso, como toda stream

```c
    fclose(file_ptr);
```

liberamos o buffer do arquivo e desconectamos ele do programa, seguindo essa base toda:

## 2. Começa hardcoded, fica dinâmico e modular.

no começo, nosso buffer, oque vamos imprimir na tela. Suporta até 256.
 
```c
buffer[256]
```

ele é uma cadeia de caracteres, uma string. oque significa que se o nosso arquivo, tiver 257 letras. Vai faltar conteúdo, é nessa hora que chegamos no maior inimigo ao enfrentar C cara a cara.

em C, "malloc" significa "Alocação de Memória" é uma função específica pra alocar memória dinâmica (runtime) dentro de um "Heap".

em C, um "Heap" é um grande espaço alocado para memória dinâmica, o problema de um "Heap", é o fato de você ter que lembrar constantemente de liberar o espaço alocado assim que terminar de usar ou pode acarretar no famoso "memory leak", que é quando seu programa perde acesso a memória "Heap" e ele começa a consumir sua memória RAM até sua máquina ficar sem memória sobrando.

ééeééééée, huuuuuuuuuuuu, tá.

lendo meu código, eu não cuidei disso ainda, mas eu apliquei essa ideia na ESTRUTURA do conteúdo do arquivo, então:

```c
    char buffer[256];
    int count = 0;

    while (fgets(buffer, sizeof(buffer), file_ptr) != NULL) {
        count++;
    }

    rewind(file_ptr); # <- Pode ignorar, depois eu explico.

    char **lines = malloc(count * sizeof(char *));
    int i = 0;
    
    while (fgets(buffer, sizeof(buffer), file_ptr) != NULL) {
        buffer[strcspn(buffer, "\n")] = '\0';
        lines[i] = malloc(strlen(buffer) + 1);
        strcpy(lines[i], buffer);
        i++;
    }
```

então, eu aloco um espaço "dinâmico" na memória, acessável através da variavel lines, onde o tamanho do espaço é: o número de caracteres de uma linha multiplicado pela quantidade de bytes de cada caractere na linha.

nisso, é agora que entra a parte mais complexa:

```c
    while (fgets(buffer, sizeof(buffer), file_ptr) != NULL) {
        buffer[strcspn(buffer, "\n")] = '\0';
        lines[i] = malloc(strlen(buffer) + 1);
        strcpy(lines[i], buffer);
        i++;
    }
```

dentro do loop, a gente começa percorrendo toda a linha dentro do buffer até chegar no primeiro "\n" (ou quebra de linha) e vai substituir pelo byte "\0" que é um terminador nulo. 

Na prática:

"Hello\n" vai virar "Hello" pois: "\n" -> "\0" oque determina que terminou aquela cadeia de caracteres.

nisso, dentro da variável lines no índice "i", nós vamos alocar espaço do tamanho da cadeia de caracteres dentro do buffer + 1. (o +1 é por que estamos contando com o "\0" no final da cadeia de caracteres e não só os caracteres)

copiamos oque está no buffer pra dentro da array: "Linhas" no índice "i" e acrescentamos 1 a "i", pra cada linha que a função fgets encontrar, ele para na quebra de linha e repete o loop até terminar.

nisso, a array Lines, vai armazenar cada linha como um valor dentro da própria array.

```teste.txt
escrevendo texto para teste
quebrando linha
```

```bash
lines[1]: escrevendo texto para teste
lines[2]: quebrando linha
```

## 3. A parte divertida, renderização, loops e como trabalhar com oque temos?

Agora, é a parte que eu mais gostaria de dar ênfase. Mas trabalhando com C até agora, percebi que eu tenho que mudar a forma como enxergo tipos. Até aqui, minha perspectiva muda de "Strings", "Inteiros", "Booleans", etc. Para Bytes. Cada caractere, botão, input, output. São apenas Bytes e nós podemos dar o valor que quisermos a eles, MESMO que ja estejam mapeados.

por padrão, o terminal ja vem pré configurado. Todo "bash" ja vem com uma configuração própria. Chamada de modo "Canonical", você pode digitar 500 caracteres, apagar, editar, até "canelar" a linha com um Ctrl + C, o input só é enviado quando vier o Enter e tudo de uma vez.

Porém, nós queremos editar um texto em tempo real, neste caso, temos que fazer umas configurações extras.

Primeiro: Salvamos as configurações anteriores.

Ja percebeu que quando você edita um arquivo no VIM, ele limpa o terminal, carrega os arquivos e depois reescreve tudo de novo? Até esse ponto, fazemos QUASE isso. Essa parte é importante:

```c
struct termios original_termios;
```

criamos uma estrutura e usando a biblioteca "termios" (ainda não sei explicar oque é de fato, só a finalidade, fica pra uma próxima pesquisa), basicamente Termios é uma biblioteca padrão em C que permite controlar terminais e outros. No nosso caso, terminais. Termios vai permitir que a gente altere os modos de entrada/saída, definir velocidade de transissão e, oque queremos, é ativar o modo "cru" onde a tecla é lida imediatamente SEM que seja necessário apertar Enter.

nisso:

```c
void disableRawMode() {
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &original_termios);
}

void enableRawMode() {
    tcgetattr(STDIN_FILENO, &original_termios);
    atexit(disableRawMode);

    struct termios raw = original_termios;

    raw.c_lflag &= ~(ECHO | ICANON);

    tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw);
}
```

disableRawMode():
- tcsetattr: altera os parâmetros do terminal
- stdin_fileno: descritor de arquivo padrão pra entrada padrão (teclado)
- tcsaflush: é a ação que aplica a mudança imediatamente, depois de transmitir a saída pendente E realiza a limpesa de qualquer entrada que AINDA não foi lida.
- &original_termios: é o ponteiro pro struct dos atributos do terminal original

enableRawMode():
- 