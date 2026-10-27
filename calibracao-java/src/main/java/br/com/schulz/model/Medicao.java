
package br.com.schulz.model;

public class Medicao {

    private int idMedicao;
    private int idEquipamento;
    private int idTecnico;
    private String parametroMedido;
    private double valorNominal;
    private double toleranciaMin;
    private double toleranciaMax;
    private double valorObtido;
    private String statusResultado;
    private String dataMedicao;

    public Medicao(int idMedicao, int idEquipamento, int idTecnico,
                   String parametroMedido, double valorNominal,
                   double toleranciaMin, double toleranciaMax,
                   double valorObtido, String statusResultado,
                   String dataMedicao) {
        this.idMedicao = idMedicao;
        this.idEquipamento = idEquipamento;
        this.idTecnico = idTecnico;
        this.parametroMedido = parametroMedido;
        this.valorNominal = valorNominal;
        this.toleranciaMin = toleranciaMin;
        this.toleranciaMax = toleranciaMax;
        this.valorObtido = valorObtido;
        this.statusResultado = validarResultado();
        this.dataMedicao = dataMedicao;
    }

    public int getIdMedicao() {
        return idMedicao;
    }

    public int getIdEquipamento() {
        return idEquipamento;
    }

    public int getIdTecnico() {
        return idTecnico;
    }

    public String getParametroMedido() {
        return parametroMedido;
    }

    public double getValorNominal() {
        return valorNominal;
    }

    public double getToleranciaMin() {
        return toleranciaMin;
    }

    public double getToleranciaMax() {
        return toleranciaMax;
    }

    public double getValorObtido() {
        return valorObtido;
    }

    public String getStatusResultado() {
        return statusResultado;
    }

    public String getDataMedicao() {
        return dataMedicao;
    }

    @Override
    public String toString() {
        return "Medicao{" +
                "idMedicao=" + idMedicao +
                ", idEquipamento=" + idEquipamento +
                ", idTecnico=" + idTecnico +
                ", parametroMedido='" + parametroMedido + '\'' +
                ", valorNominal=" + valorNominal +
                ", toleranciaMin=" + toleranciaMin +
                ", toleranciaMax=" + toleranciaMax +
                ", valorObtido=" + valorObtido +
                ", statusResultado='" + statusResultado + '\'' +
                ", dataMedicao='" + dataMedicao + '\'' +
                '}';
    }

    public String validarResultado() {
        if (valorObtido >= toleranciaMin
                && valorObtido <= toleranciaMax) {
            return "APROVADO";
        }

        return "REPROVADO";
    }

}
