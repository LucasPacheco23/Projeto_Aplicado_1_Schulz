
package br.com.schulz.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import br.com.schulz.model.Medicao;

public class MedicaoDAO {

    public List<Medicao> listarTodos() throws SQLException {
        String sql = """
                SELECT id_medicao, id_equipamento, id_tecnico,
                       parametro_medido, valor_nominal,
                       tolerancia_min, tolerancia_max,
                       valor_obtido, status_resultado, data_medicao
                FROM medicao
                ORDER BY data_medicao DESC
                """;

        List<Medicao> medicoes = new ArrayList<>();

        try (Connection conexao = ConexaoBanco.conectar();
             PreparedStatement comando = conexao.prepareStatement(sql);
             ResultSet resultado = comando.executeQuery()) {

            while (resultado.next()) {
                Medicao medicao = new Medicao(
                    resultado.getInt("id_medicao"),
                    resultado.getInt("id_equipamento"),
                    resultado.getInt("id_tecnico"),
                    resultado.getString("parametro_medido"),
                    resultado.getDouble("valor_nominal"),
                    resultado.getDouble("tolerancia_min"),
                    resultado.getDouble("tolerancia_max"),
                    resultado.getDouble("valor_obtido"),
                    resultado.getString("status_resultado"),
                    resultado.getString("data_medicao")
                );

                medicoes.add(medicao);
            }
        }

        return medicoes;
    }

    
    public void inserir(Medicao medicao) throws SQLException {
        String sql = """
                INSERT INTO medicao (
                    id_equipamento,
                    id_tecnico,
                    parametro_medido,
                    valor_nominal,
                    tolerancia_min,
                    tolerancia_max,
                    valor_obtido,
                    status_resultado
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """;

        try (Connection conexao = ConexaoBanco.conectar();
             PreparedStatement comando = conexao.prepareStatement(sql)) {

            comando.setInt(1, medicao.getIdEquipamento());
            comando.setInt(2, medicao.getIdTecnico());
            comando.setString(3, medicao.getParametroMedido());
            comando.setDouble(4, medicao.getValorNominal());
            comando.setDouble(5, medicao.getToleranciaMin());
            comando.setDouble(6, medicao.getToleranciaMax());
            comando.setDouble(7, medicao.getValorObtido());
            comando.setString(8, medicao.getStatusResultado());

            comando.executeUpdate();
        }
    }

    
    public void listarRelatorioCalibracao() throws SQLException {
        String sql = """
                SELECT
                    m.id_medicao,
                    e.codigo_tag,
                    e.nome_equipamento,
                    t.nome_tecnico,
                    m.parametro_medido,
                    m.valor_nominal,
                    m.tolerancia_min,
                    m.tolerancia_max,
                    m.valor_obtido,
                    m.status_resultado,
                    m.data_medicao
                FROM medicao m
                INNER JOIN equipamento e
                    ON m.id_equipamento = e.id_equipamento
                INNER JOIN tecnico t
                    ON m.id_tecnico = t.id_tecnico
                ORDER BY m.data_medicao DESC
                """;

        try (Connection conexao = ConexaoBanco.conectar();
             PreparedStatement comando = conexao.prepareStatement(sql);
             ResultSet resultado = comando.executeQuery()) {

            System.out.println("\n===== RELATÓRIO DE CALIBRAÇÃO =====");

            boolean encontrouRegistros = false;

            while (resultado.next()) {
                encontrouRegistros = true;

                System.out.println("----------------------------------");
                System.out.println("Medição: "
                        + resultado.getInt("id_medicao"));
                System.out.println("Equipamento: "
                        + resultado.getString("codigo_tag")
                        + " - "
                        + resultado.getString("nome_equipamento"));
                System.out.println("Técnico: "
                        + resultado.getString("nome_tecnico"));
                System.out.println("Parâmetro: "
                        + resultado.getString("parametro_medido"));
                System.out.println("Valor nominal: "
                        + resultado.getDouble("valor_nominal"));
                System.out.println("Tolerância mínima: "
                        + resultado.getDouble("tolerancia_min"));
                System.out.println("Tolerância máxima: "
                        + resultado.getDouble("tolerancia_max"));
                System.out.println("Valor obtido: "
                        + resultado.getDouble("valor_obtido"));
                System.out.println("Resultado: "
                        + resultado.getString("status_resultado"));
                System.out.println("Data: "
                        + resultado.getString("data_medicao"));
            }

            if (!encontrouRegistros) {
                System.out.println("Nenhuma medição cadastrada.");
            }

            System.out.println("===== FIM DO RELATÓRIO =====\n");
        }
    }

    
    public boolean existeMedicao(
            int idEquipamento,
            int idTecnico,
            String parametroMedido) throws SQLException {

        String sql = """
                SELECT COUNT(*)
                FROM medicao
                WHERE id_equipamento = ?
                  AND id_tecnico = ?
                  AND parametro_medido = ?
                """;

        try (Connection conexao = ConexaoBanco.conectar();
             PreparedStatement comando = conexao.prepareStatement(sql)) {

            comando.setInt(1, idEquipamento);
            comando.setInt(2, idTecnico);
            comando.setString(3, parametroMedido);

            try (ResultSet resultado = comando.executeQuery()) {
                return resultado.next() && resultado.getInt(1) > 0;
            }
        }
    }

    
    public boolean atualizar(Medicao medicao) throws SQLException {
        String sql = """
                UPDATE medicao
                SET id_equipamento = ?,
                    id_tecnico = ?,
                    parametro_medido = ?,
                    valor_nominal = ?,
                    tolerancia_min = ?,
                    tolerancia_max = ?,
                    valor_obtido = ?,
                    status_resultado = ?
                WHERE id_medicao = ?
                """;

        try (Connection conexao = ConexaoBanco.conectar();
             PreparedStatement comando = conexao.prepareStatement(sql)) {

            comando.setInt(1, medicao.getIdEquipamento());
            comando.setInt(2, medicao.getIdTecnico());
            comando.setString(3, medicao.getParametroMedido());
            comando.setDouble(4, medicao.getValorNominal());
            comando.setDouble(5, medicao.getToleranciaMin());
            comando.setDouble(6, medicao.getToleranciaMax());
            comando.setDouble(7, medicao.getValorObtido());
            comando.setString(8, medicao.validarResultado());
            comando.setInt(9, medicao.getIdMedicao());

            return comando.executeUpdate() > 0;
        }
    }

    
    public boolean excluir(int idMedicao) throws SQLException {
        String sql = """
                DELETE FROM medicao
                WHERE id_medicao = ?
                """;

        try (Connection conexao = ConexaoBanco.conectar();
             PreparedStatement comando = conexao.prepareStatement(sql)) {

            comando.setInt(1, idMedicao);

            return comando.executeUpdate() > 0;
        }
    }

}
