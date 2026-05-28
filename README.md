<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0f172a,100:1e40af&height=180&section=header&text=Jogo%20Battleship&fontSize=38&fontColor=ffffff&animation=fadeIn&fontAlignY=35"/>

<h1 align="center">⚓ Batalha Naval (Battleship)</h1>
<h3 align="center">Desenvolvimento de Software • Algoritmos Estruturados • Python</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Ambiente-Terminal-black?style=for-the-badge" alt="Terminal" />
  <img src="https://img.shields.io/badge/PUCPR-Ciência%20da%20Computação-red?style=for-the-badge" alt="PUCPR" />
</p>

---

## 📝 Sobre o Projeto

Este projeto consiste na implementação do clássico jogo **Batalha Naval (Battleship)** desenvolvido em Python. O software simula o confronto estratégico entre dois tabuleiros, onde o objetivo principal é mapear a grade adversária e interceptar toda a frota inimiga antes de ter seus próprios navios naufragados.

O desenvolvimento foi focado na aplicação prática de estruturas de dados lineares e bidimensionais, modularização de código através de funções e tratamento rigoroso de exceções para garantir uma experiência de usuário fluida via terminal.

---

## 🚀 Funcionalidades Principais

- 🗺️ **Mapeamento de Coordenadas:** Renderização dinâmica de matrizes bidimensionais para representar o oceano e os tabuleiros (Jogador vs. IA/Máquina).
- 🚢 **Posicionamento de Frota:** Algoritmo de validação para alocação de navios de forma estratégica, prevenindo sobreposição de estruturas ou estouro dos limites cartesianos.
- 🎯 **Sistema de Disparos Integrado:** Computação de ataques baseada na entrada de coordenadas (Linha x Coluna), com feedback em tempo real de acertos ("Água" ou "Fogo!").
- 🤖 **Modo Inteligente (IA):** Sistema automatizado para os turnos da máquina, realizando escolhas aleatórias ou semi-estratégicas de ataque.
- 📊 **Placar Dinâmico:** Monitoramento contínuo da integridade das frotas e exibição do progresso do jogo a cada rodada.

---

## 🛠️ Tecnologias e Conceitos Aplicados

O projeto explora conceitos fundamentais de lógica de programação e arquitetura básica de software:

- **Matrizes e Vetores:** Uso intensivo de listas compostas em Python para gerenciar o estado oculto e visível dos tabuleiros.
- **Estruturas de Repetição e Condicionais:** Laços `while` e `for` estruturados para controle do fluxo de turnos e varredura de coordenadas.
- **Modularização:** Divisão da lógica de jogo em funções com responsabilidades únicas (geração de tela, validação de tiro, checagem de vitória).
- **Sanitização de Entradas:** Tratamento de erros para impedir que inputs inválidos do usuário quebrem a execução do programa em tempo real.