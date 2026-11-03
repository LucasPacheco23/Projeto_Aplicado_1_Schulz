# ==============================================================================
# UNIDADE CURRICULAR: PROJETO APLICADO I
# EMPRESA PARCEIRA: SCHULZ S.A.
# SCRIPT DE GERAÇÃO AUTOMÁTICA DA DOCUMENTAÇÃO EM MARKDOWN (01_estrutura.md)
# ==============================================================================
conteudo_markdown = """# PROJETO APLICADO I - SCHULZ S.A.
## Entrega 02: Modelagem e Estruturação de Banco de Dados Relacional
**Integrantes da Equipe:** Bruno Henridson Galvão, Lucas Jean Pacheco, Mateus Junior Consoli, Rodrigo Nunes, Sthefane Passos Pita
**Data de Entrega:** 18/10/2026
**Orientadores:** Prof. MSc. Hugo Menezes Barra | Prof. Rodrigo Losina
---
### 1. Contexto e Problematização (Transição de Planilhas para BD)
Na Entrega 01, identificamos que a gestão dos certificados de calibração da **Schulz
S.A.** baseava-se em planilhas Excel manuais e descentralizadas. Esse modelo
operacional apresenta sérios riscos operacionais:
- **Risco de Perda de Histórico:** Falta de rastreabilidade de medições e calibrações
passadas.
- **Inconsistência e Duplicação:** Inserção redundante do mesmo equipamento ou
técnico em múltiplos arquivos.
- **Falha na Segurança e Integridade:** Vulnerabilidade a alterações indevidas sem
auditoria.
A migração para um **Banco de Dados Relacional (SQLite)** garantirá a centralização
dos dados, integridade referencial e facilidade na recuperação de informações
críticas para os processos de qualidade.
---
### 2. Divisão do Banco de Dados em Entidades Principais
Para eliminar a redundância e organizar a arquitetura da informação, o banco de dados
foi estruturado nas 3 entidades fundamentais a seguir:
#### 2.1. Entidade 1: TECNICO / SOLICITANTE
- **Função:** Armazena os dados cadastrais dos técnicos e colaboradores responsáveis
pelas medições e calibrações.
- **Atributos Previstos:** `id_tecnico` (Chave Primária), `nome`, `cargo`,
`departamento`.
#### 2.2. Entidade 2: EQUIPAMENTO
- **Função:** Registra os instrumentos e máquinas da fábrica submetidos a controle e
aferição contínua.
- **Atributos Previstos:** `id_equipamento` (Chave Primária), `tag_identificacao`,
`nome_equipamento`, `modelo`, `data_aquisicao`.
#### 2.3. Entidade 3: MEDICÃO / CALIBRAÇÃO
- **Função:** Entidade transacional que registra o evento de medição, conectando o
técnico ao equipamento avaliado.
- **Atributos Previstos:** `id_medicao` (Chave Primária), `id_equipamento` (Chave
Estrangeira), `id_tecnico` (Chave Estrangeira), `data_medicao`, `valor_medido`,
`status_aprovacao`, `observacoes`.
---
### 3. Justificativa da Eliminação de Dados Duplicados
A normalização do banco de dados em entidades separadas resolve os principais
problemas mapeados na Fase 01:
1. **Atendimentos às Normas de Qualidade:** Cada calibração fica permanentemente
associada ao histórico do equipamento e ao técnico responsável.
2. **Otimização do Armazenamento:** Dados de técnicos e equipamentos são cadastrados
apenas uma vez, evitando repetir cada medição.
3. **Integridade Referencial:** Impede o registro de medições para equipamentos
inexistentes ou por técnicos não cadastrados.
---
### 4. Próximos Passos (Implementação DDL no SQLite)
A partir dessa estrutura conceitual definida, a próxima etapa consistirá na criação
dos scripts SQL (`CREATE TABLE`) para materializar o banco de dados
`schulz_calibracao.db` via Python.
"""
# Execução da gravação do arquivo .md
nome_arquivo = "01_estrutura.md"
try:
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo_markdown)
    print("=" * 60)
    print(f"SUCCESS: O arquivo '{nome_arquivo}' foi gerado com sucesso!")
    print("Abra o VS Code, selecione o arquivo e pressione 'Ctrl + Shift + V'")
    print("para visualizar a documentacao formatada.")
    print("=" * 60)
except Exception as e:
    print(f"ERRO ao gerar o arquivo: {e}")