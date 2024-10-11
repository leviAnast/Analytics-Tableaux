# Projeto de Prova por Tableaux Analíticos

Este projeto implementa um algoritmo para verificar a validade de sequentes lógicos através do método de prova por tableaux analíticos. O algoritmo processa fórmulas proposicionais em formato de entrada e valida sequentes, retornando uma valoração de átomos caso o tableau não feche, ou confirmando o sequente como válido caso feche.

## Funcionalidades

- **Expansão de Fórmulas Alfa e Beta:** O algoritmo realiza a expansão de fórmulas do tipo alfa e beta.
- **Checagem de Fechamento do Ramo:** Verifica se o ramo contém átomos contraditórios, fechando o ramo.
- **Valoração dos Átomos:** Em caso de ramo aberto, imprime a valoração dos átomos.
- **Leitura de Arquivo de Entrada:** Lê as fórmulas a partir de um arquivo de entrada e as processa como parte do ramo inicial.

## Estrutura do Projeto

- `modulos/` - Contém módulos auxiliares, como o `Tableaux` e o `SubformulaExtractor`.
- `main.py` - Executa o algoritmo principal de prova por tableaux.
- `README.md` - Este documento, com instruções e descrições do projeto.

## Pré-requisitos

- Python 3.x
- Bibliotecas:
  - `lark`: para o parser de fórmulas proposicionais.

Para instalar a biblioteca `lark`, execute o comando:

```bash
pip install lark
