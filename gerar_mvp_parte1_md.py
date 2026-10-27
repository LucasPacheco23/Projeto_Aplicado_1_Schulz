# ==============================================================================
# UNIDADE CURRICULAR: PROJETO APLICADO I
# EMPRESA PARCEIRA: SCHULZ S.A.
# SCRIPT DE GERAÇÃO DA DOCUMENTAÇÃO DO MVP - PARTE 1
# Arquivo gerado: 06_mvp_parte1.md
# ==============================================================================

from pathlib import Path

conteudo_markdown = """# MVP — Parte 1: Sistema de Calibração Schulz S.A.

**Unidade Curricular:** Projeto Aplicado I  
**Empresa parceira:** Schulz S.A.  
**Entrega:** AV03 — Construção do MVP (Parte 1)  
**Linguagem:** Java  
**Banco de dados:** SQLite  
**Acesso ao banco:** JDBC

---

## 1. Objetivo

Esta etapa implementa a primeira versão funcional de um sistema de calibração, utilizando programação orientada a objetos em Java e persistência de dados em SQLite.

O sistema representa técnicos, equipamentos e medições de calibração. Também calcula o resultado de uma medição com base nos limites mínimo e máximo aceitáveis e apresenta um relatório que relaciona os registros das três entidades.

## 2. Organização do projeto

O código Java está organizado no projeto Maven `calibracao-java`.

```text
calibracao-java/
├── pom.xml
└── src/
    └── main/
        └── java/
            └── br/
                └── com/
                    └── schulz/
                        ├── Main.java
                        ├── dao/
                        │   ├── ConexaoBanco.java
                        │   ├── TecnicoDAO.java
                        │   ├── EquipamentoDAO.java
                        │   └── MedicaoDAO.java
                        └── model/
                            ├── Tecnico.java
                            ├── Equipamento.java
                            └── Medicao.java
```

Os arquivos de banco de dados, scripts Python e documentos das etapas anteriores permanecem na pasta principal do projeto.

## 3. Programação orientada a objetos

### 3.1. Classe `Tecnico`

Representa o profissional responsável pela medição. Seus atributos incluem identificador, nome, matrícula, e-mail e setor.

A classe encapsula esses dados por meio de atributos privados e métodos de acesso.

### 3.2. Classe `Equipamento`

Representa o instrumento ou equipamento submetido à calibração. Contém identificador, código de identificação (tag), nome, fabricante e modelo.

### 3.3. Classe `Medicao`

Representa o registro de uma medição. Seus atributos incluem os identificadores do equipamento e do técnico, parâmetro medido, valor nominal, limites mínimo e máximo, valor obtido, resultado e data da medição.

O método `validarResultado()` aplica a regra:

- `APROVADO`: quando o valor obtido está entre os limites mínimo e máximo, inclusive.
- `REPROVADO`: quando o valor obtido está fora desse intervalo.

O resultado é calculado pela classe a partir dos valores da medição.

### 3.4. Classes de acesso a dados (DAO)

As classes `TecnicoDAO`, `EquipamentoDAO` e `MedicaoDAO` concentram as operações SQL referentes às respectivas entidades.

A classe `ConexaoBanco` centraliza a abertura da conexão JDBC com o banco SQLite.

Essa separação mantém as responsabilidades de domínio, persistência e execução principal organizadas.

## 4. Diagrama textual das classes

```text
Main
 ├── TecnicoDAO
 ├── EquipamentoDAO
 └── MedicaoDAO
       └── ConexaoBanco

Tecnico
 └── idTecnico, nomeTecnico, matricula, email, setor

Equipamento
 └── idEquipamento, codigoTag, nomeEquipamento,
     fabricante, modelo

Medicao
 └── idMedicao, idEquipamento, idTecnico,
     parametroMedido, valorNominal, toleranciaMin,
     toleranciaMax, valorObtido, statusResultado,
     dataMedicao
       └── validarResultado()
```

Relacionamentos no banco:

- Um técnico pode estar associado a várias medições.
- Um equipamento pode estar associado a várias medições.
- Cada medição referencia um técnico e um equipamento.

## 5. Persistência com SQLite

O sistema utiliza JDBC para se conectar ao arquivo `schulz_calibracao.db`.

As classes DAO utilizam comandos SQL preparados (`PreparedStatement`) para executar operações de persistência.

As operações implementadas incluem:

- **INSERT:** inserção de técnicos, equipamentos e medições.
- **SELECT:** listagem e busca de técnicos e equipamentos, listagem de medições e consulta do relatório.
- **UPDATE:** atualização de técnicos, equipamentos e medições.
- **DELETE:** exclusão de técnicos, equipamentos e medições.

Os métodos de atualização e exclusão retornam um valor booleano indicando se alguma linha foi afetada.

A exclusão de registros relacionados pode ser impedida pelas restrições de integridade referencial do banco.

## 6. Consulta relacional e relatório

O método `listarRelatorioCalibracao()` da classe `MedicaoDAO` utiliza `INNER JOIN` entre as tabelas de medições, equipamentos e técnicos.

O relatório apresenta o identificador da medição, código e nome do equipamento, nome do técnico, parâmetro medido, valor nominal, limites de tolerância, valor obtido, resultado e data.

Essa consulta demonstra a recuperação conjunta de informações relacionadas no banco relacional.

## 7. Tratamento de erros SQL

As operações de persistência declaram a possibilidade de ocorrência de `SQLException`.

As conexões, instruções SQL e resultados de consulta são gerenciados com `try-with-resources`, que fecha os recursos automaticamente ao final do bloco.

A classe `Main` captura exceções SQL e apresenta uma mensagem de erro no terminal. Isso permite informar falhas de execução sem encerrar o fluxo com uma exceção não tratada nesse ponto.

## 8. Validação do fluxo funcional

A classe `Main` coordena a demonstração do sistema:

1. Localiza o técnico de demonstração pela matrícula.
2. Localiza o equipamento pela tag.
3. Verifica se já existe uma medição para a combinação de equipamento, técnico e parâmetro utilizada na demonstração.
4. Insere a medição caso essa combinação ainda não exista.
5. Consulta as quantidades de técnicos, equipamentos e medições.
6. Executa a consulta relacional e apresenta o relatório de calibração.

A verificação da medição é específica para o fluxo de demonstração. Ela não substitui uma regra geral de unicidade para todas as medições.

### Resultado observado na execução

Na execução realizada no VS Code, o Maven concluiu o programa com `BUILD SUCCESS`.

O terminal apresentou:

- 1 técnico cadastrado;
- 1 equipamento cadastrado;
- 1 medição cadastrada;
- valor nominal de 10,0;
- limite mínimo de 9,5;
- limite máximo de 10,5;
- valor obtido de 10,1;
- resultado `APROVADO`.

O relatório exibiu os dados relacionados do equipamento e do técnico. O valor obtido estava dentro do intervalo aceitável, conforme a regra implementada.

A compilação bem-sucedida também foi verificada após a inclusão dos métodos de atualização e exclusão. Essas operações ainda devem ser testadas individualmente antes de serem consideradas validadas em execução.

## 9. Considerações finais

A implementação estabelece a estrutura inicial do MVP de calibração com Java, orientação a objetos e persistência SQLite.

A separação entre modelos, classes DAO e classe principal facilita a manutenção do código. A validação da medição e a consulta com `JOIN` demonstram o fluxo central da aplicação.

Como próximos passos, recomenda-se validar individualmente as operações de atualização e exclusão em dados controlados, revisar as regras de integridade do banco e consolidar o material explicativo solicitado para a entrega.

## 10. Execução do sistema

A partir da pasta `calibracao-java`, executar:

```powershell
mvn clean compile
mvn exec:java "-Dexec.mainClass=br.com.schulz.Main"
```

O banco SQLite utilizado está na pasta principal do projeto, um nível acima de `calibracao-java`.
"""

# Localiza a pasta onde este script está salvo.
pasta_projeto = Path(__file__).resolve().parent
caminho_saida = pasta_projeto / "06_mvp_parte1.md"

# Gera o arquivo Markdown em UTF-8.
with open(caminho_saida, "w", encoding="utf-8") as arquivo:
    arquivo.write(conteudo_markdown)

print("Documentação do MVP - Parte 1 gerada com sucesso!")
print(f"Arquivo criado em: {caminho_saida}")