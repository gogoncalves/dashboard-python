package dominio

import java.time.LocalDate

data class Leitura(
    var fkRegiao: Int,
    var fkEstado: Int,
    var fkCidade: Int,
    var fkEquipamento: Int,
    var fkComponente: Int,
    var valor: Double,
    var momento: LocalDate
) {
    constructor() : this(0, 0, 0, 0, 0, 0.0, LocalDate.parse("YYYY-MM-dd"))
}