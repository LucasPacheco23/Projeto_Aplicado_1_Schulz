
package br.com.schulz;

import java.sql.SQLException;
import java.util.List;

import br.com.schulz.dao.TecnicoDAO;
import br.com.schulz.model.Tecnico;

public class TesteCadastroTecnico {

    public static void main(String[] args) {

        TecnicoDAO tecnicoDAO = new TecnicoDAO();

        Tecnico tecnico = new Tecnico(
            0,
            "Tecnico de Teste",
            "TESTE001",
            "teste@exemplo.com",
            "Calibracao"
        );

        try {
            tecnicoDAO.inserir(tecnico);

            System.out.println("Técnico cadastrado com sucesso!");
            System.out.println();

            List<Tecnico> tecnicos = tecnicoDAO.listarTodos();

            System.out.println("=== TÉCNICOS CADASTRADOS ===");

            for (Tecnico cadastrado : tecnicos) {
                System.out.println(cadastrado);
            }

        } catch (SQLException e) {
            System.err.println("Erro ao cadastrar ou consultar técnico.");
            System.err.println("Detalhes: " + e.getMessage());
        }
    }
}
