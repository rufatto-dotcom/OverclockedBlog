---
title: Como eu aprendi 5 linguagens de programação em 1 ano
tag: Leve
date: jun 2026
---

## Como aprender qualquer coisa de forma rápida

Não é segredo pra todos que eu sou obcecado (talvez maluco) pela área da computação. Se somar todo o tempo de estudo que eu tenho, sentado com a bundinha na cadeira estudando, passa facilmente das 4.500 horas, quase 5.000 horas.

- Mas afinal de contas Rufatto, como isso te faz aprender rápido?

Assim como tudo na vida, você jamais pode se contentar em saber fazer. É só isso, em vez de aprender como fazer o carro andar, pergunte-se depois, por que ele anda?

Parece chatisse, mas é assim que você é capaz de aprender qualquer coisa. E digo mais, quanto mais você sabe o por que das coisas, mais rápido ainda você vai aprender o por que de outras.

Pensa em alguém que decora a receita de bolo de cor — segue o passo a passo certinho, mas se faltar um ingrediente ou o forno for diferente, trava. Agora pensa em alguém que entende o que cada ingrediente faz (por que o fermento sobe, por que o ovo liga a massa). Essa pessoa improvisa, troca, conserta — porque ela não aprendeu "os passos", ela aprendeu "o porquê dos passos".

## Que tal um exemplo na prática?

Veja, eu tenho um protótipo de Processador feito a mão com placas de teste. Sim, um Processador, aquele chip caro que vai no meio da sua placa mãe, feito por máquinas tão precisas que é impossível de enxergar os componentes^[Componentes são peças que se conectam em um eletrônico e tem algum tipo de função quando recebem energia], isso por si só, me ensinou como a máquina pensa, sabe aquela máquina nada importante?

- O computador?

Sim, é, só esse carinha ai que usamos todo dia pra quase tudo. Bom, todo Processador possui uma linguagem onde você é capaz de dar instruções pro sistema MANUALMENTE. Ja ouviu falar do "Assembly"^[Linguagem de programação de baixo nível que representa diretamente as instruções nativas de um processador], acredite ou não, a maioria das linguagens de programação do mercado, quando compiladas em um executável^[Executável é o arquivo final que o sistema operacional consegue rodar diretamente, sem precisar de mais nenhuma tradução] de fato, simplesmente viram Assembly (Instruções diretas pro processador).

- Então, se tudo no fim das contas vira a mesma coisa, basta entender como funciona?

Bom, vamos começar de cima, da camada mais "confortável", e ir descendo até chegar no metal de verdade. PHP é um bom ponto de partida porque grande parte da web ainda roda escondida atrás dele:

```PHP
<?php

fwrite(STDOUT, "Mensagem no Terminal" . PHP_EOL);
```

Esta linha de código, vai ser COMPILADA (explico em outro post como funciona a compilação de um código) e quando executado, vai imprimir "Mensagem no Terminal" no terminal

O mesmo recado, em Python, fica ainda mais curto — é praticamente a frase em português, só com parênteses:

```Python
print("Mensagem no Terminal")
```

Faz a exata mesma coisa, só muda a forma como escrevi, engraçado não? Agora repara como o Java já exige um pouco mais de "burocracia" antes de chegar no que realmente importa:

```JAVA
public class Main {
    public static void main(String args[]) {
        System.out.println("Mensagem no terminal")
    }
}
```

JAVA parece pior, mas é só por quê ele exige que o programa seja executado dentro de uma classe main (Dedicarei um blog só pra isso, é um assunto muito legal). Mas vamos saindo da nuvem e descendo pro chão — C já te deixa bem mais perto do hardware, sem tanta camada de proteção no meio do caminho:

```C
#include <stdio.h>

int main(void) {
    printf("Mensagem no terminal")

    return 0
}
```

Sinceramente, posso passar o dia aqui escrevendo. Mas tenham em mente que todos esses exemplos, no fim, executam a mesma coisa — e aqui embaixo de tudo, sem mais nenhuma camada pra descer, é onde a viagem termina:

```Assembly
section .data
    msg db "Mensagem no Terminal", 0xa
    msg_len equ $ - msg

section .text
    global _start

_start:
    mov rax, 1          ; syscall número 1 = write
    mov rdi, 1          ; primeiro argumento: fd 1 = stdout
    mov rsi, msg        ; segundo argumento: endereço da string
    mov rdx, msg_len    ; terceiro argumento: quantos bytes escrever
    syscall

    mov rax, 60         ; syscall número 60 = exit
    mov rdi, 0          ; código de saída 0
    syscall
```

Esse último `syscall`^[Syscall é um pedido direto pro sistema operacional fazer algo que o programa não pode fazer por conta própria, como escrever na tela] é o que efetivamente fecha o programa.

E essa é a parte mais bonita disso tudo: programa não tem sotaque, programa só tem uma fala.

Assim como na vida real, se você souber falar 10 línguas, você ainda vai estar falando a mesma coisa, a mesma frase, só muda como você pronuncia^[Pronunciar aqui no sentido de sintaxe — a regra de como você escreve aquilo que quer dizer]. Um bom programador é aquele que escolhe falar Russo com Russos, e não escolhe falar só Inglês porque é "confortável".

## Mas e as ferramentas do mercado? E em outras áreas?

Não entendeu ainda? Pergunte

- Pra você?

Não pra mim, pra quem está te ensinando, pesquise na IA, pesquise no Google, questione o por quê das coisas serem como são, garanto que quando você entender o porque as coisas são como são, o resto se desenrola facilmente.

Vejo vocês na proxima! PS: Espero que tenha ficado bom as mensagens no rodapé, tentei pegar um assunto mais divertido