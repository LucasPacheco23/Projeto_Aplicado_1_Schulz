
package br.com.schulz.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import br.com.schulz.model.Tecnico;

public class TecnicoDAO {

    public List<Tecnico> listarTodos() throws SQLException {
        String sql = """
                SELECT id_tecnico, nome_tecnico, matricula, email, setor
                FROM tecnico
                ORDER BY nome_tecnico
                """;

        List<Tecnico> tecnicos = new ArrayList<>();

        try (Connection conexao = ConexaoBanco.conectar();
             PreparedStatement comando = conexao.prepareStatement(sql);
             ResultSet resultado = comando.executeQuery()) {

            while (resultado.next()) {
                Tecnico tecnico = new Tecnico(
                    resultado.getInt("id_tecnico"),
                    resultado.getString("nome_tecnico"),
                    resultado.getString("matricula"),
                    resultado.getString("email"),
                    resultado.getString("setor")
                );

                tecnicos.add(tecnico);
            }
        }

        return tecnicos;
    }

    
    public void inserir(Tecnico tecnico) throws SQLException {
        String sql = """
                INSERT INTO tecnico
                    (nome_tecnico, matricula, email, setor)
                VALUES (?, ?, ?, ?)
                """;

        try (Connection conexao = ConexaoBanco.conectar();
             PreparedStatement comando = conexao.prepareStatement(sql)) {

            comando.setString(1, tecnico.getNomeTecnico());
            comando.setString(2, tecnico.getMatricula());
            comando.setString(3, tecnico.getEmail());
            comando.setString(4, tecnico.getSetor());

            comando.executeUpdate();
        }
    }

    
    public Tecnico buscarPorMatricula(String matricula) throws SQLException {
        String sql = """
                SELECT id_tecnico, nome_tecnico, matricula, email, setor
                FROM tecnico
                WHERE matricula = ?
                """;

        try (Connection conexao = ConexaoBanco.conectar();
             PreparedStatement comando = conexao.prepareStatement(sql)) {

            comando.setString(1, matricula);

            try (ResultSet resultado = comando.executeQuery()) {
                if (resultado.next()) {
                    return new Tecnico(
                        resultado.getInt("id_tecnico"),
                        resultado.getString("nome_tecnico"),
                        resultado.getString("matricula"),
                        resultado.getString("email"),
                        resultado.getString("setor")
                    );
                }
            }
        }

        return null;
    }

    
    public boolean atualizar(Tecnico tecnico) throws SQLException {
        String sql = """
                UPDATE tecnico
                SET nome_tecnico = ?,
                    matricula = ?,
                    email = ?,
                    setor = ?
                WHERE id_tecnico = ?
                """;

        try (Connection conexao = ConexaoBanco.conectar();
             PreparedStatement comando = conexao.prepareStatement(sql)) {

            comando.setString(1, tecnico.getNomeTecnico());
            comando.setString(2, tecnico.getMatricula());
            comando.setString(3, tecnico.getEmail());
            comando.setString(4, tecnico.getSetor());
            comando.setInt(5, tecnico.getIdTecnico());

            return comando.executeUpdate() > 0;
        }
    }

    
    public boolean excluir(int idTecnico) throws SQLException {
        String sql = """
                DELETE FROM tecnico
                WHERE id_tecnico = ?
                """;

        try (Connection conexao = ConexaoBanco.conectar();
             PreparedStatement comando = conexao.prepareStatement(sql)) {

            comando.setInt(1, idTecnico);

            return comando.executeUpdate() > 0;
        }
    }

}
