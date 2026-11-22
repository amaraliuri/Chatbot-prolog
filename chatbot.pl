% Carrega a base de conhecimento externa
:- consult('dados.pl').

% Dividir a entrada em tokens
tokenizar_frase(Frase, Tokens) :-
    split_string(Frase, ' ', '', Tokens).

% Conta quantas palavras da frase aparecem
contar_correspondencias([], _, 0).
contar_correspondencias([Palavra|Resto], Pergunta, Pontos) :-
    contar_correspondencias(Resto, Pergunta, PontosResto),
    (   sub_string(Pergunta, _, _, _, Palavra)
    ->  Pontos is PontosResto + 1
    ;   Pontos is PontosResto
    ).

% Encontrar a melhor correspondência pela quantidade de palavras em comum
encontrar_correspondencia([], _, 'Desculpe, não entendi sua pergunta.') :- !.
encontrar_correspondencia(Tokens, ListaPerguntas, Resposta) :-
    findall(Pontos-Pergunta, (
        member(Pergunta, ListaPerguntas),
        contar_correspondencias(Tokens, Pergunta, Pontos),
        Pontos > 0
    ), Pontuacoes),
    (   Pontuacoes = []
    ->  Resposta = 'Desculpe, não entendi sua pergunta.'
    ;   sort(1, @>=, Pontuacoes, [_-MelhorPergunta|_]),
        pergunta_resposta(MelhorPergunta, Resposta)
    ).

% Função para responder perguntas
responder_pergunta(Frase, Resposta) :-
    atomics_to_string(Frase, ' ', FraseString),
    tokenizar_frase(FraseString, Tokens),
    findall(P, pergunta_resposta(P, _), ListaPerguntas),
    encontrar_correspondencia(Tokens, ListaPerguntas, Resposta).

% Chatbot interativo
chatbot :-
    write('Pergunte algo: '), nl,
    read(Entrada),
    (   Entrada = sair
    ->  write('Até mais!'), nl
    ;   atomics_to_string(ListaEntrada, ' ', Entrada),
        responder_pergunta(ListaEntrada, Resposta),
        write(Resposta), nl,
        chatbot
    ).

 % py interface.py