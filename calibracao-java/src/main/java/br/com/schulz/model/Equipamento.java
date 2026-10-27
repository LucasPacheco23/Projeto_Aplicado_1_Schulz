
package br.com.schulz.model;

public class Equipamento {

    private int idEquipamento;
    private String codigoTag;
    private String nomeEquipamento;
    private String fabricante;
    private String modelo;

    public Equipamento(int idEquipamento, String codigoTag,
                       String nomeEquipamento, String fabricante,
                       String modelo) {
        this.idEquipamento = idEquipamento;
        this.codigoTag = codigoTag;
        this.nomeEquipamento = nomeEquipamento;
        this.fabricante = fabricante;
        this.modelo = modelo;
    }

    public int getIdEquipamento() {
        return idEquipamento;
    }

    public String getCodigoTag() {
        return codigoTag;
    }

    public String getNomeEquipamento() {
        return nomeEquipamento;
    }

    public String getFabricante() {
        return fabricante;
    }

    public String getModelo() {
        return modelo;
    }

    @Override
    public String toString() {
        return "Equipamento{" +
                "idEquipamento=" + idEquipamento +
                ", codigoTag='" + codigoTag + '\'' +
                ", nomeEquipamento='" + nomeEquipamento + '\'' +
                ", fabricante='" + fabricante + '\'' +
                ", modelo='" + modelo + '\'' +
                '}';
    }
}
