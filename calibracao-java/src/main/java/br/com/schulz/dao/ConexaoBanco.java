
package br.com.schulz.dao;

import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class ConexaoBanco {

    private static final Path CAMINHO_BANCO = Path.of(
        "..", "schulz_calibracao.db"
    ).toAbsolutePath().normalize();

    private static final String URL_BANCO =
        "jdbc:sqlite:" + CAMINHO_BANCO;

    public static Connection conectar() throws SQLException {
        return DriverManager.getConnection(URL_BANCO);
    }

    public static void main(String[] args) {
        System.out.println("Caminho do banco: " + CAMINHO_BANCO);

        try (Connection conexao = conectar()) {
            System.out.println("Conexão com SQLite estabelecida!");
            System.out.println("Banco fechado ao final do teste.");
        } catch (SQLException e) {
            System.err.println("Erro ao conectar ao banco SQLite.");
            System.err.println("Detalhes: " + e.getMessage());
        }
    }
}
