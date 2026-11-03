# 02_dicionario.md — Dicionário de Dados do Sistema
**Unidade Curricular:** Projeto Aplicado I
**Empresa Parceira:** Schulz S.A.
**Tema 02:** Modelagem e Implementação de Banco de Dados (SQLite)
**Professores:** Prof. MSc. Hugo Menezes Barra | Prof. Rodrigo Losina
---
## 1. Mapeamento das Tabelas e Campos
### 1.1. Tabela: `tecnico` (Técnicos / Solicitantes)
| Nome do Campo | Tipo (SQLite) | Restrições / Chaves | Descrição / Regra de Negócio |
| :--- | :--- | :--- | :--- |
| `id_tecnico` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único do técnico. |
| `nome_tecnico` | TEXT | NOT NULL | Nome completo do profissional. |
| `setor` | TEXT | NOT NULL | Departamento de atuação (Ex: Metrologia). |
### 1.2. Tabela: `equipamento` (Instrumentos e Máquinas)
| Nome do Campo | Tipo (SQLite) | Restrições / Chaves | Descrição / Regra de Negócio |
| :--- | :--- | :--- | :--- |
| `id_equipamento` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único do equipamento.
|
| `codigo_tag` | TEXT | NOT NULL, UNIQUE | Código/Tag gravado no instrumento. |
| `nome_equipamento`| TEXT | NOT NULL | Descrição do equipamento (Ex: Paquímetro). |
| `fabricante` | TEXT | NOT NULL | Fabricante (Ex: Mitutoyo, Starrett). |
| `modelo` | TEXT | NOT NULL | Modelo do instrumento. |
### 1.3. Tabela: `medicao` (Registro das Calibrações / Ensaios)
| Nome do Campo | Tipo (SQLite) | Restrições / Chaves | Descrição / Regra de Negócio |
| :--- | :--- | :--- | :--- |
| `id_medicao` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único do ensaio. |
| `id_equipamento` | INTEGER | FOREIGN KEY (equipamento) | Vínculo com o equipamento avaliado.
|
| `id_tecnico` | INTEGER | FOREIGN KEY (tecnico) | Vínculo com o técnico responsável. |
| `parametro_medido` | TEXT | NOT NULL | Variável aferida (Ex: Comprimento, Pressão). |
| `valor_nominal` | REAL | NOT NULL | Valor de referência padrão esperado. |
| `tolerancia_min` | REAL | NOT NULL | Limite inferior aceitável. |
| `tolerancia_max` | REAL | NOT NULL | Limite superior aceitável. |
| `valor_obtido` | REAL | NOT NULL | Leitura real coletada no ensaio. |
| `status_resultado`| TEXT | CHECK ('APROVADO', 'REPROVADO') | Parecer técnico automático. |
| `data_medicao` | TEXT / DATETIME | DEFAULT CURRENT_TIMESTAMP | Data e hora automática da
calibração. |
