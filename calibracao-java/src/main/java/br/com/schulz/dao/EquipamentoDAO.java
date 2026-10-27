
package br.com.schulz.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import br.com.schulz.model.Equipamento;

public class EquipamentoDAO {

    public List<Equipamento> listarTodos() throws SQLException {
        String sql = """
                SELECT id_equipamento, codigo_tag, nome_equipamento,
                       fabricante, modelo
                FROM equipamento
                ORDER BY codigo_tag
                """;

        List<Equipamento> equipamentos = new ArrayList<>();

        try (Connection conexao = ConexaoBanco.conectar();
             PreparedStatement comando = conexao.prepareStatement(sql);
             ResultSet resultado = comando.executeQuery()) {

            while (resultado.next()) {
                Equipamento equipamento = new Equipamento(
                    resultado.getInt("id_equipamento"),
                    resultado.getString("codigo_tag"),
                    resultado.getString("nome_equipamento"),
                    resultado.getString("fabricante"),
                    resultado.getString("modelo")
                );

                equipamentos.add(equipamento);
            }
        }

        return equipamentos;
    }

    public void inserir(Equipamento equipamento) throws SQLException {
        String sql = """
                INSERT INTO equipamento (
                    codigo_tag,
                    nome_equipamento,
                    fabricante,
                    modelo
                ) VALUES (?, ?, ?, ?)
                """;

        try (Connection conexao = ConexaoBanco.conectar();
             PreparedStatement comando = conexao.prepareStatement(sql)) {

            comando.setString(1, equipamento.getCodigoTag());
            comando.setString(2, equipamento.getNomeEquipamento());
            comando.setString(3, equipamento.getFabricante());
            comando.setString(4, equipamento.getModelo());

            comando.executeUpdate();
        }
    }

    
    public Equipamento buscarPorCodigoTag(String codigoTag)
            throws SQLException {

        String sql = """
                SELECT id_equipamento, codigo_tag, nome_equipamento,
                       fabricante, modelo
                FROM equipamento
                WHERE codigo_tag = ?
                """;

        try (Connection conexao = ConexaoBanco.conectar();
             PreparedStatement comando = conexao.prepareStatement(sql)) {

            comando.setString(1, codigoTag);

            try (ResultSet resultado = comando.executeQuery()) {
                if (resultado.next()) {
                    return new Equipamento(
                        resultado.getInt("id_equipamento"),
                        resultado.getString("codigo_tag"),
                        resultado.getString("nome_equipamento"),
                        resultado.getString("fabricante"),
                        resultado.getString("modelo")
                    );
                }
            }
        }

        return null;
    }

    
    public boolean atualizar(Equipamento equipamento) throws SQLException {
        String sql = """
                UPDATE equipamento
                SET codigo_tag = ?,
                    nome_equipamento = ?,
                    fabricante = ?,
                    modelo = ?
                WHERE id_equipamento = ?
                """;

        try (Connection conexao = ConexaoBanco.conectar();
             PreparedStatement comando = conexao.prepareStatement(sql)) {

            comando.setString(1, equipamento.getCodigoTag());
            comando.setString(2, equipamento.getNomeEquipamento());
            comando.setString(3, equipamento.getFabricante());
            comando.setString(4, equipamento.getModelo());
            comando.setInt(5, equipamento.getIdEquipamento());

            return comando.executeUpdate() > 0;
        }
    }

    
    public boolean excluir(int idEquipamento) throws SQLException {
        String sql = """
                DELETE FROM equipamento
                WHERE id_equipamento = ?
                """;

        try (Connection conexao = ConexaoBanco.conectar();
             PreparedStatement comando = conexao.prepareStatement(sql)) {

            comando.setInt(1, idEquipamento);

            return comando.executeUpdate() > 0;
        }
    }

}
