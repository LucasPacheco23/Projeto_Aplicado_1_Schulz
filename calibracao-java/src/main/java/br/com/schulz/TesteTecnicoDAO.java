
package br.com.schulz;

import java.sql.SQLException;
import java.util.List;

import br.com.schulz.dao.TecnicoDAO;
import br.com.schulz.model.Tecnico;

public class TesteTecnicoDAO {

    public static void main(String[] args) {
        TecnicoDAO tecnicoDAO = new TecnicoDAO();

        try {
            List<Tecnico> tecnicos = tecnicoDAO.listarTodos();

            System.out.println("=== TÉCNICOS CADASTRADOS ===");
            System.out.println("Quantidade encontrada: " + tecnicos.size());
            System.out.println();

            for (Tecnico tecnico : tecnicos) {
                System.out.println(tecnico);
            }

        } catch (SQLException e) {
            System.err.println("Erro ao consultar os técnicos.");
            System.err.println("Detalhes: " + e.getMessage());
        }
    }
}

