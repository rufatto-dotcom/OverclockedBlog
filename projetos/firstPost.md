---
title: como eu aprendi a não ter medo do malloc
tag: C
date: jun 2026
---

## o problema com buffer[256]

eu comecei lendo arquivo com um `buffer[256]`, bem cru, bem hardcoded.

```c
char buffer[256];
```

funciona, até o arquivo ter uma linha com 257 caracteres. nesse momento o programa simplesmente não vai ler tudo, e foi aí que eu fui obrigado a conhecer o maior inimigo de quem encara C de frente: alocação dinâmica.

## heap, malloc e o medo que isso me deu

"malloc" é alocação de memória. é uma função pra pedir espaço dentro do "Heap", que é tipo um terreno baldio gigante que o sistema te dá, mas com uma pegadinha: você tem que lembrar de devolver esse espaço depois.

se você esquecer, é o famoso memory leak: seu programa vai consumindo RAM até a máquina implorar misericórdia.

ééééééééééé.... eu ainda não tratei isso no meu código (eu sei, eu sei), mas pelo menos já aplico a lógica certa pra guardar o conteúdo do arquivo.

## guardando cada linha na memória

a ideia: primeiro eu conto quantas linhas o arquivo tem, sem fazer nada com elas ainda.

```c
char buffer[256];
int count = 0;

while (fgets(buffer, sizeof(buffer), file_ptr) != NULL) {
    count++;
}

rewind(file_ptr); // volta o "cursor" do arquivo pro início
```

com o número de linhas em mãos, eu aloco um array de ponteiros — `lines` — do tamanho certo:

```c
char **lines = malloc(count * sizeof(char *));
int i = 0;

while (fgets(buffer, sizeof(buffer), file_ptr) != NULL) {
    buffer[strcspn(buffer, "\n")] = '\0';
    lines[i] = malloc(strlen(buffer) + 1);
    strcpy(lines[i], buffer);
    i++;
}
```

a parte que mais me confundiu foi essa aqui:

```c
buffer[strcspn(buffer, "\n")] = '\0';
```

`strcspn` acha a posição do primeiro `\n` na linha, e eu troco esse caractere por `\0` (terminador nulo). na prática: `"hello\n"` vira `"hello"`. sem isso, cada linha guardada ia carregar a quebra de linha junto, o que é meio inútil.

depois disso, pra cada linha: aloco espaço do tamanho exato dela (+1 por causa do `\0`), copio o conteúdo pra dentro de `lines[i]` e sigo pra próxima.

resultado: um `teste.txt` desses

```
escrevendo texto para teste
quebrando linha
```

vira isso na memória:

```
lines[0]: escrevendo texto para teste
lines[1]: quebrando linha
```

cada linha, seu próprio espacinho na memória, do tamanho que ela realmente precisa. nada de desperdício, nada de hardcode.

(o memory leak que eu disse que ainda não resolvi? fica pro próximo post)