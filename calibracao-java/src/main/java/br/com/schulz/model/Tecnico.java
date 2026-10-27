
package br.com.schulz.model;

public class Tecnico {

    private int idTecnico;
    private String nomeTecnico;
    private String matricula;
    private String email;
    private String setor;

    public Tecnico(int idTecnico, String nomeTecnico,
                   String matricula, String email, String setor) {
        this.idTecnico = idTecnico;
        this.nomeTecnico = nomeTecnico;
        this.matricula = matricula;
        this.email = email;
        this.setor = setor;
    }

    public int getIdTecnico() {
        return idTecnico;
    }

    public String getNomeTecnico() {
        return nomeTecnico;
    }

    public String getMatricula() {
        return matricula;
    }

    public String getEmail() {
        return email;
    }

    public String getSetor() {
        return setor;
    }

    @Override
    public String toString() {
        return "Tecnico{" +
                "idTecnico=" + idTecnico +
                ", nomeTecnico='" + nomeTecnico + '\'' +
                ", matricula='" + matricula + '\'' +
                ", email='" + email + '\'' +
                ", setor='" + setor + '\'' +
                '}';
    }
}
