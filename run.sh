#!/bin/bash

#Leitora
fluxo_1_feliz_leitora=('Oi' 'Leitora' 'Sim' 'ATM voltou a funcionar' 'Não')
fluxo_2_perguntas=('Oi' 'Leitora' 'Sim' 'ATM voltou a funcionar' 'Sim')
fluxo_3_palavra_trocada=('Oi' 'Leitora' 'Sim' 'ATM ainda não operante' 'Não' 'Não')
fluxo_4_nao_operante=('Oi' 'Leitora' 'Sim' 'ATM ainda não operante' 'ATM ainda não operante' 'Não')
fluxo_5_nao_operante=('Oi' 'Leitora' 'Sim' 'ATM ainda não operante' 'ATM ainda não operante' 'Sim')
fluxo_6_nenhuma_das_alternativas=('Oi' 'Leitora' 'Não' 'Não')
fluxo_7_nda_sem_finalizar=('Oi' 'Leitora' 'Não' 'Sim')

# id=$(uuidgen)

echo "Apresentando a conversa com a Dani fluxo feliz"

Nome_Arq_fluxo="fluxo_1_feliz_leitora"
id=$(uuidgen)
for ((i = 0; i <= 4; i += 1)); do
    echo "${fluxo_1_feliz_leitora[i]}"
    correlation_id=$(uuidgen)
    echo "Novo id de correlacao = ${correlation_id}"      
    python3 sender.py ${correlation_id} ${id} ${fluxo_1_feliz_leitora[i]} >> Saidas_Leitora/$Nome_Arq_fluxo.json
    python3 receiver.py ${correlation_id} >> Saidas_Leitora/$Nome_Arq_fluxo.json
done

echo "Apresentando a conversa com o bot fluxo 2"

Nome_Arq_fluxo="fluxo_2_perguntas"
id=$(uuidgen)
for ((i = 0; i <= 4; i += 1)); do
    echo "${fluxo_2_perguntas[i]}"
    correlation_id=$(uuidgen)
    echo "Novo id de correlacao = ${correlation_id}"
    python3 sender.py ${correlation_id} ${id} ${fluxo_2_perguntas[i]} >> Saidas_Leitora/$Nome_Arq_fluxo.json
    python3 receiver.py ${correlation_id}  >> Saidas_Leitora/$Nome_Arq_fluxo.json
done

echo "Apresentando a conversa com o bot fluxo 3"

Nome_Arq_fluxo="fluxo_3_palavra_trocada"
id=$(uuidgen)
for ((i = 0; i <= 5; i += 1)); do
    echo "${fluxo_3_palavra_trocada[i]}"
    correlation_id=$(uuidgen)
    echo "Novo id de correlacao = ${correlation_id}"
    python3 sender.py ${correlation_id} ${id} ${fluxo_3_palavra_trocada[i]} >> Saidas_Leitora/$Nome_Arq_fluxo.json
    python3 receiver.py  >> Saidas_Leitora/$Nome_Arq_fluxo.json
done

echo "Apresentando a conversa com o bot fluxo 4"

Nome_Arq_fluxo="fluxo_4_nao_operante"
id=$(uuidgen)
for ((i = 0; i <= 5; i += 1)); do
    echo "${fluxo_4_nao_operante[i]}"
    correlation_id=$(uuidgen)
    echo "Novo id de correlacao = ${correlation_id}"
    python3 sender.py ${correlation_id} ${id} ${fluxo_4_nao_operante[i]} >> Saidas_Leitora/$Nome_Arq_fluxo.json
    python3 receiver.py  >> Saidas_Leitora/$Nome_Arq_fluxo.json
done

# echo "Apresentando a conversa com o bot fluxo 5"

# Nome_Arq_fluxo="fluxo_5_nao_operante"
# id=$(uuidgen)
# for ((i = 0; i <= 5; i += 1)); do
#     echo "${fluxo_5_nao_operante[i]}"
#     python3 sender.py ${id} ${fluxo_5_nao_operante[i]} >> Saidas_Leitora/$Nome_Arq_fluxo.txt
#     python3 receiver.py  >> Saidas_Leitora/$Nome_Arq_fluxo.txt
# done

# echo "Apresentando a conversa com o bot fluxo 6"

# Nome_Arq_fluxo="fluxo_6_nenhuma_das_alternativas"
# id=$(uuidgen)
# for ((i = 0; i <= 3; i += 1)); do
#     echo "${fluxo_6_nenhuma_das_alternativas[i]}"
#     python3 sender.py ${id} ${fluxo_6_nenhuma_das_alternativas[i]} >> Saidas_Leitora/$Nome_Arq_fluxo.txt
#     python3 receiver.py  >> Saidas_Leitora/$Nome_Arq_fluxo.txt
# done

# echo "Apresentando a conversa com o bot fluxo 7"

# Nome_Arq_fluxo="fluxo_7_nda_sem_finalizar"
# id=$(uuidgen)
# for ((i = 0; i <= 3; i += 1)); do
#     echo "${fluxo_7_nda_sem_finalizar[i]}"
#     python3 sender.py ${id} ${fluxo_7_nda_sem_finalizar[i]} >> Saidas_Leitora/$Nome_Arq_fluxo.txt
#     python3 receiver.py  >> Saidas_Leitora/$Nome_Arq_fluxo.txt
# done