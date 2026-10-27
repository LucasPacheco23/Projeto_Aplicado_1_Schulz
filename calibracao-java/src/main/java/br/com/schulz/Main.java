
package br.com.schulz;

import java.sql.SQLException;
import java.util.List;

import br.com.schulz.dao.EquipamentoDAO;
import br.com.schulz.dao.MedicaoDAO;
import br.com.schulz.dao.TecnicoDAO;
import br.com.schulz.model.Equipamento;
import br.com.schulz.model.Medicao;
import br.com.schulz.model.Tecnico;

public class Main {

    public static void main(String[] args) {
        System.out.println("==================================");
        System.out.println(" SISTEMA DE CALIBRAÇÃO - SCHULZ");
        System.out.println("==================================");

        try {
            TecnicoDAO tecnicoDAO = new TecnicoDAO();
            EquipamentoDAO equipamentoDAO = new EquipamentoDAO();
            MedicaoDAO medicaoDAO = new MedicaoDAO();

            // 1. Localizar o técnico de demonstração.
            Tecnico tecnico =
                    tecnicoDAO.buscarPorMatricula("TESTE001");

            if (tecnico == null) {
                tecnico = new Tecnico(
                        0,
                        "Tecnico de Demonstracao",
                        "DEMO001",
                        "demo@exemplo.com",
                        "Calibracao"
                );

                tecnicoDAO.inserir(tecnico);

                tecnico = tecnicoDAO.buscarPorMatricula("DEMO001");
            }

            if (tecnico == null) {
                throw new SQLException(
                        "Não foi possível localizar o técnico de demonstração."
                );
            }

            // 2. Localizar ou cadastrar o equipamento de demonstração.
            Equipamento equipamento =
                    equipamentoDAO.buscarPorCodigoTag("EQ-DEMO-001");

            if (equipamento == null) {
                equipamento = new Equipamento(
                        0,
                        "EQ-DEMO-001",
                        "Equipamento de Demonstracao",
                        "Schulz",
                        "MODELO-DEMO"
                );

                equipamentoDAO.inserir(equipamento);

                equipamento =
                        equipamentoDAO.buscarPorCodigoTag("EQ-DEMO-001");
            }

            if (equipamento == null) {
                throw new SQLException(
                        "Não foi possível localizar o equipamento de demonstração."
                );
            }

            // 3. Inserir a medição somente se ela ainda não existir.
            String parametro = "Pressao";

            boolean medicaoExiste = medicaoDAO.existeMedicao(
                    equipamento.getIdEquipamento(),
                    tecnico.getIdTecnico(),
                    parametro
            );

            if (!medicaoExiste) {
                Medicao medicao = new Medicao(
                        0,
                        equipamento.getIdEquipamento(),
                        tecnico.getIdTecnico(),
                        parametro,
                        10.0,
                        9.5,
                        10.5,
                        10.1,
                        "",
                        null
                );

                medicaoDAO.inserir(medicao);

                System.out.println(
                        "\nMedição de demonstração cadastrada."
                );
                System.out.println(
                        "Resultado calculado: "
                                + medicao.getStatusResultado()
                );
            } else {
                System.out.println(
                        "\nA medição de demonstração já existe; "
                                + "nenhuma nova medição foi inserida."
                );
            }

            // 4. Exibir o resumo dos registros.
            List<Tecnico> tecnicos = tecnicoDAO.listarTodos();
            List<Equipamento> equipamentos =
                    equipamentoDAO.listarTodos();
            List<Medicao> medicoes = medicaoDAO.listarTodos();

            System.out.println("\n===== RESUMO DO BANCO =====");
            System.out.println("Técnicos cadastrados: " + tecnicos.size());
            System.out.println(
                    "Equipamentos cadastrados: " + equipamentos.size()
            );
            System.out.println("Medições cadastradas: " + medicoes.size());

            // 5. Exibir relatório com JOIN entre as tabelas.
            medicaoDAO.listarRelatorioCalibracao();

        } catch (SQLException e) {
            System.err.println(
                    "Erro ao executar o sistema de calibração."
            );
            System.err.println("Detalhes: " + e.getMessage());
        }
    }
}
