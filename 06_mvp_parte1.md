# PROJETO APLICADO I - SCHULZ S.A.

## AV03: Construção do MVP (Parte 1)

**Unidade Curricular:** Projeto Aplicado I

**Empresa Parceira:** Schulz S.A.

**Linguagem de Programação:** Python

**Banco de Dados:** SQLite

**Professores:** Prof. MSc. Hugo Menezes Barra | Prof. Rodrigo Losina

---

## 1. Objetivo do MVP

O objetivo desta etapa é implementar a primeira versão funcional do sistema
de calibração da Schulz S.A., utilizando Programação Orientada a Objetos (POO)
em Python e conexão com um banco de dados relacional SQLite.

Nas etapas anteriores, foram desenvolvidos os arquivos de documentação da
estrutura do projeto, o dicionário de dados e o script SQL responsável pela
criação das tabelas do banco.

Nesta etapa, o projeto evolui para a implementação das classes de domínio,
da camada de persistência e de um programa principal para demonstrar o
funcionamento do sistema.

O MVP permite representar técnicos, equipamentos e medições, validar dados,
calcular a média e o desvio padrão de duas leituras e registrar resultados
no banco de dados.

A aprovação implementada nesta versão considera a média das duas leituras
em relação aos limites mínimo e máximo de tolerância cadastrados.

Esta versão representa a primeira parte do sistema. A importação de planilhas
Excel, o cálculo completo de incerteza e a geração automática dos certificados
de calibração não fazem parte do escopo implementado nesta etapa.

---

## 2. Estrutura dos arquivos

O código foi organizado em arquivos separados para facilitar a manutenção
e separar as responsabilidades de cada componente.

A estrutura relevante para a AV03 é apresentada a seguir:

```text
versao_python/
|
|-- classes/
|   |-- __init__.py
|   |-- tecnico.py
|   |-- equipamento.py
|   |-- medicao.py
|   |-- banco_dados.py
|
|-- 05_main.py
|-- gerar_mvp_parte1_md.py
|-- 06_mvp_parte1.md
|-- 03_banco.sql
|-- executar_banco.py
|-- schulz_calibracao.db
```

### 2.1. Responsabilidade dos arquivos

| Arquivo | Responsabilidade |
| :--- | :--- |
| `tecnico.py` | Define a classe `Tecnico` e valida os dados cadastrais do profissional. |
| `equipamento.py` | Define a classe `Equipamento` e valida os dados do equipamento. |
| `medicao.py` | Define a classe `Medicao`, calcula estatísticas e avalia o resultado por tolerância. |
| `banco_dados.py` | Centraliza a conexão SQLite e as operações de persistência e consulta. |
| `__init__.py` | Expõe as classes do pacote para facilitar as importações. |
| `05_main.py` | Executa a demonstração funcional, cadastra dados de teste e apresenta o relatório. |
| `03_banco.sql` | Contém as instruções SQL para a estrutura relacional do banco. |
| `schulz_calibracao.db` | Armazena os registros persistidos no SQLite. |
| `gerar_mvp_parte1_md.py` | Gera automaticamente esta documentação em Markdown. |

---

## 3. Programação Orientada a Objetos (POO)

A implementação utiliza classes e objetos para representar as entidades
principais do sistema.

### 3.1. Classe Tecnico

A classe `Tecnico`, definida em `classes/tecnico.py`, representa o profissional
responsável pelas atividades de medição e calibração.

Seus atributos são:

- `id_tecnico`: identificador do técnico no banco de dados.
- `nome_tecnico`: nome do profissional.
- `matricula`: matrícula única do profissional.
- `email`: endereço de e-mail.
- `setor`: setor de atuação.

O método `validar()` verifica se os campos obrigatórios foram preenchidos.

### 3.2. Classe Equipamento

A classe `Equipamento`, definida em `classes/equipamento.py`, representa a
máquina ou o instrumento submetido à calibração.

Seus atributos são:

- `id_equipamento`: identificador do equipamento no banco de dados.
- `codigo_tag`: código de identificação único do equipamento.
- `nome_equipamento`: nome ou descrição do equipamento.
- `fabricante`: fabricante do equipamento.
- `modelo`: modelo do equipamento.

O método `validar()` verifica o preenchimento dos campos obrigatórios.

### 3.3. Classe Medicao

A classe `Medicao`, definida em `classes/medicao.py`, representa o registro
de uma avaliação de um parâmetro do equipamento.

Seus atributos incluem:

- `id_medicao`: identificador da medição.
- `id_equipamento`: referência ao equipamento avaliado.
- `id_tecnico`: referência ao técnico responsável.
- `parametro_medido`: descrição do parâmetro avaliado.
- `valor_nominal`: valor de referência.
- `tolerancia_min`: limite inferior aceitável.
- `tolerancia_max`: limite superior aceitável.
- `medida_1`: primeira leitura realizada.
- `medida_2`: segunda leitura realizada.

A classe disponibiliza as seguintes propriedades e métodos:

- `validar()`: verifica os dados da medição e a consistência do intervalo
  de tolerância.
- `media`: calcula a média aritmética das duas leituras.
- `desvio_padrao`: calcula o desvio padrão amostral das duas leituras.
- `status_resultado`: retorna `APROVADO` quando a média está dentro dos
  limites de tolerância, inclusive nos limites, ou `REPROVADO` caso contrário.

Nesta implementação, `tolerancia_min` e `tolerancia_max` representam
diretamente os limites inferior e superior da faixa aceitável.

O cálculo do desvio padrão utiliza a função `stdev` do módulo `statistics`
da biblioteca padrão do Python.

### 3.4. Classe BancoDados

A classe `BancoDados`, definida em `classes/banco_dados.py`, é responsável
pelo acesso ao banco SQLite.

Suas responsabilidades incluem:

- Abrir conexões com o banco de dados.
- Ativar a verificação de chaves estrangeiras nas conexões.
- Inserir registros de técnicos, equipamentos e medições.
- Consultar técnicos e equipamentos por seus identificadores únicos.
- Consultar medições relacionadas a técnicos e equipamentos.
- Atualizar registros existentes.
- Executar consultas relacionais por meio de `INNER JOIN`.

Essa separação evita concentrar as instruções SQL nas classes de domínio
e facilita a manutenção do acesso aos dados.

---

## 4. Diagrama textual das classes

O diagrama abaixo representa as principais classes e seus relacionamentos
no MVP implementado.

```text
+-----------------------+
|        Tecnico        |
+-----------------------+
| id_tecnico            |
| nome_tecnico          |
| matricula             |
| email                 |
| setor                 |
+-----------------------+
| validar()             |
+-----------------------+
           |
           | 1
           |
           | N
+-----------------------+       +-----------------------+
|        Medicao        |       |      Equipamento      |
+-----------------------+       +-----------------------+
| id_medicao            |       | id_equipamento        |
| id_tecnico            |       | codigo_tag            |
| id_equipamento        |       | nome_equipamento      |
| parametro_medido      |       | fabricante            |
| valor_nominal         |       | modelo                |
| tolerancia_min        |       +-----------------------+
| tolerancia_max        |                   |
| medida_1              |                   | 1
| medida_2              |                   |
+-----------------------+                   | N
| validar()             |                   |
| media                 |                   |
| desvio_padrao         |                   |
| status_resultado      |                   |
+-----------------------+-------------------+

+------------------------------------------+
|                BancoDados                |
+------------------------------------------+
| caminho                                  |
+------------------------------------------+
| conectar()                               |
| salvar_tecnico()                         |
| buscar_tecnico()                         |
| atualizar_tecnico()                      |
| salvar_equipamento()                     |
| buscar_equipamento()                     |
| atualizar_equipamento()                  |
| salvar_medicao()                         |
| atualizar_medicao()                      |
| listar_medicoes()                        |
+------------------------------------------+
```

**Interpretação do diagrama:**

- Um técnico pode estar relacionado a várias medições.
- Um equipamento pode estar relacionado a várias medições.
- Cada medição está vinculada a um técnico e a um equipamento.
- `BancoDados` executa as operações de persistência utilizadas pelas
  classes e pelo programa principal.

As associações entre as entidades são implementadas por chaves estrangeiras
na tabela `medicao`.

---

## 5. Persistência e integridade no SQLite

O banco de dados utilizado é o arquivo `schulz_calibracao.db`, com três
tabelas principais: `tecnico`, `equipamento` e `medicao`.

### 5.1. Chaves primárias e estrangeiras

Cada tabela possui uma chave primária para identificar seus registros.

A tabela `medicao` possui as chaves estrangeiras `id_equipamento` e
`id_tecnico`, que estabelecem o relacionamento com as tabelas de equipamento
e técnico, respectivamente.

Esses relacionamentos permitem consultar os dados de uma medição juntamente
com as informações do equipamento e do profissional responsável.

### 5.2. Operações SQL

A camada de persistência utiliza as seguintes operações:

| Operação | Finalidade |
| :--- | :--- |
| `INSERT` | Inserir técnicos, equipamentos e medições. |
| `SELECT` | Consultar registros individuais e listar medições. |
| `UPDATE` | Atualizar dados de técnicos, equipamentos e medições. |
| `INNER JOIN` | Relacionar medições aos seus equipamentos e técnicos. |

As consultas utilizam parâmetros SQL para separar os valores fornecidos
das instruções executadas.

O uso de `PRAGMA foreign_keys = ON` nas conexões habilita a verificação
das chaves estrangeiras pelo SQLite.

A implementação atual não possui um método de exclusão (`DELETE`) na
camada `BancoDados`. Essa operação poderá ser acrescentada em uma evolução
posterior, respeitando as restrições de integridade referencial.

### 5.3. Gerenciamento das transações

As operações de escrita utilizam o gerenciamento de transações do SQLite.
Quando uma operação termina corretamente, a transação é confirmada.
Se ocorrer uma exceção durante a transação, o SQLite desfaz as alterações
daquela transação.

As conexões são fechadas após as operações por meio do gerenciador
de contexto `closing`.

---

## 6. Validação das regras de negócio

A validação é executada antes de persistir os objetos no banco.

### 6.1. Validação do técnico

O método `validar()` verifica se nome, matrícula, e-mail e setor foram
preenchidos.

### 6.2. Validação do equipamento

O método `validar()` verifica se código TAG, nome do equipamento,
fabricante e modelo foram preenchidos.

### 6.3. Validação da medição

O método `validar()` verifica:

- Se o parâmetro avaliado foi informado.
- Se os valores utilizados nos cálculos são numéricos e finitos.
- Se o limite inferior não é superior ao limite máximo.
- Se os identificadores do técnico e do equipamento são válidos.

### 6.4. Avaliação por tolerância

A propriedade `status_resultado` compara a média das duas leituras com
os limites mínimo e máximo informados.

A regra implementada é:

```text
Se tolerancia_min <= media <= tolerancia_max:
    Resultado = APROVADO
Caso contrário:
    Resultado = REPROVADO
```

Essa regra corresponde à avaliação inicial por tolerância. Ela não
representa, isoladamente, uma decisão metrológica completa que considere
incerteza de medição ou regras adicionais da empresa.

---

## 7. Tratamento de erros

O programa principal `05_main.py` utiliza tratamento de exceções para
identificar falhas durante a execução.

| Exceção | Tratamento |
| :--- | :--- |
| `ValueError` | Informa problemas de validação dos dados. |
| `sqlite3.IntegrityError` | Informa violações de integridade do banco, como restrições de unicidade ou de chaves estrangeiras. |
| `sqlite3.Error` | Informa erros relacionados ao SQLite. |
| `OSError` | Informa falhas de acesso a arquivos ou ao sistema operacional. |

O tratamento de exceções impede que essas falhas sejam apresentadas
simplesmente como resultados normais do programa.

As mensagens exibidas no terminal ajudam a identificar a categoria do
problema ocorrido.

---

## 8. Fluxo funcional do MVP

O arquivo `05_main.py` demonstra o fluxo básico de utilização do sistema.

1. Inicializa a camada de acesso ao banco de dados.
2. Consulta a existência do técnico reservado para demonstração.
3. Consulta a existência do equipamento reservado para demonstração.
4. Cria os registros de demonstração somente quando necessário.
5. Verifica se a medição de demonstração já foi registrada.
6. Instancia um objeto `Medicao` com duas leituras e seus limites de tolerância.
7. Calcula a média e o desvio padrão e avalia o resultado.
8. Persiste a medição no SQLite, quando ainda não existe.
9. Executa uma consulta com `INNER JOIN`.
10. Exibe no terminal um relatório com os dados das medições cadastradas.

A demonstração utiliza registros identificados especificamente para teste,
sem representar resultados reais de calibração.

A verificação dos registros de demonstração evita repetir os mesmos
cadastros a cada execução normal do programa.

---

## 9. Como executar e validar

A aplicação pode ser executada pelo terminal integrado do VS Code.

Na pasta `versao_python`, execute:

```powershell
py -m py_compile 05_main.py classes\__init__.py classes\tecnico.py classes\equipamento.py classes\medicao.py classes\banco_dados.py
```

Em seguida, execute:

```powershell
py 05_main.py
```

A execução deve demonstrar o cadastro ou a reutilização dos dados de teste,
o cálculo da média e do desvio padrão, a avaliação por tolerância e a
exibição do relatório de medições.

Para o exemplo de demonstração utilizado no programa:

- Valor nominal: 10,00.
- Limite mínimo: 9,90.
- Limite máximo: 10,10.
- Primeira leitura: 10,02.
- Segunda leitura: 10,04.
- Média: 10,03.
- Resultado por tolerância: APROVADO.

A documentação pode ser visualizada no VS Code utilizando
**Ctrl + Shift + V**.

---

## 10. Limitações e próximos passos

O MVP implementado atende à primeira etapa de estruturação das classes,
validação inicial, persistência e demonstração de consultas relacionais.

As seguintes funcionalidades ainda não estão implementadas nesta versão:

- Importação dos parâmetros diretamente da planilha Excel.
- Persistência individual das duas leituras e do desvio padrão.
- Cálculo completo da incerteza de medição conforme o processo da empresa.
- Geração automática do certificado de calibração.
- Exclusão de registros por meio de métodos específicos de persistência.

Essas funcionalidades não devem ser consideradas concluídas nesta entrega.

A evolução posterior deverá preservar a integridade do banco e validar as
regras de negócio antes de gerar documentos de calibração.

---

## 11. Conclusão

A AV03 representa a transição da modelagem do banco de dados para a
implementação de uma primeira versão funcional do sistema.

A utilização de classes separadas, a centralização das operações SQL,
a validação dos dados e a demonstração de consultas relacionais estabelecem
uma base organizada para as próximas etapas do projeto.

A implementação atual permite demonstrar os fundamentos de POO em Python,
a persistência no SQLite e a avaliação inicial de medições por tolerância,
mantendo explícitas as funcionalidades que ainda precisam ser desenvolvidas.
