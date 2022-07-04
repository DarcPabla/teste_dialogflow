#!/bin/bash

#Leitora
fluxo_1_feliz_leitora=('Oi' 'Leitora' 'Sim' 'ATM voltou a funcionar' 'Não')
fluxo_2_perguntas=('Oi' 'Leitora' 'Sim' 'ATM voltou a funcionar' 'Sim')
fluxo_3_perguntas=('Oi' 'Leitora' 'Sim' 'ATM ainda não operante' 'Não')
fluxo_4_nao_operante=('Oi' 'Leitora' 'Sim' 'ATM ainda não operante' 'ATM ainda não operante')

id=$(uuidgen)

echo "Apresentando a conversa com a Dani fluxo feliz"

Nome_Arq_fluxo="leitora"
#id=$(uuidgen)
for ((i = 0; i <= 4; i += 1)); do
    echo "${fluxo_1_feliz_leitora[i]}"
    python3 sender.py ${id} ${fluxo_1_feliz_leitora[i]} >> Saidas_Leitora/$Nome_Arq_fluxo.txt
    python3 receiver.py  >> Saidas_Leitora/$Nome_Arq_fluxo.txt
done

echo "Apresentando a conversa com o bot fluxo 2"

Nome_Arq_fluxo="fluxo_2_perguntas"
#id=$(uuidgen)
for ((i = 0; i <= 4; i += 1)); do
    echo "${fluxo_2_perguntas[i]}"
    python3 sender.py ${id} ${fluxo_2_perguntas[i]} >> Saidas_Leitora/$Nome_Arq_fluxo.txt
    python3 receiver.py  >> Saidas_Leitora/$Nome_Arq_fluxo.txt
done

echo "Apresentando a conversa com o bot fluxo 3"

Nome_Arq_fluxo="fluxo_3_perguntas"
#id=$(uuidgen)
for ((i = 0; i <= 4; i += 1)); do
    echo "${fluxo_3_perguntas[i]}"
    python3 sender.py ${id} ${fluxo_3_perguntas[i]} >> Saidas_Leitora/$Nome_Arq_fluxo.txt
    python3 receiver.py  >> Saidas_Leitora/$Nome_Arq_fluxo.txt
done

echo "Apresentando a conversa com o bot fluxo 4"

Nome_Arq_fluxo="fluxo_4_nao_operante"
#id=$(uuidgen)
for ((i = 0; i <= 4; i += 1)); do
    echo "${fluxo_4_nao_operante[i]}"
    python3 sender.py ${id} ${fluxo_4_nao_operante[i]} >> Saidas_Leitora/$Nome_Arq_fluxo.txt
    python3 receiver.py  >> Saidas_Leitora/$Nome_Arq_fluxo.txt
done