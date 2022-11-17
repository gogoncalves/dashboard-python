package repositorio

import dominio.Leitura
import org.springframework.jdbc.core.BeanPropertyRowMapper
import org.springframework.jdbc.core.JdbcTemplate
import java.sql.Connection

class LeituraRepositorio(val jdbcTemplate: JdbcTemplate, val jdbcTemplateMySQL: Connection) {
    fun inserir(leitura: Leitura) {
        jdbcTemplate.update("""
            INSERT INTO GustavoLeitura (fkRegiao, fkEstado, fkCidade, fkEquipamento, fkComponente, valor, momento) values
            (?, ?, ?, ?, ?, ?, ?)
        """, leitura.fkRegiao, leitura.fkEstado,leitura.fkCidade,leitura.fkEquipamento,leitura.fkComponente, leitura.valor, leitura.momento)

        jdbcTemplateMySQL.prepareStatement("""
            INSERT INTO GustavoLeitura (fkRegiao, fkEstado, fkCidade, fkEquipamento, fkComponente, valor, momento) values
            (${leitura.fkRegiao}, ${leitura.fkEstado}, ${leitura.fkCidade},${leitura.fkEquipamento},${leitura.fkComponente}, ${leitura.valor}, curdate())
        """).execute()
    }

    fun regiao(i: Int):List<Leitura> {
        return jdbcTemplate.query("select fkRegiao from GustavoEquipamento where idEquipamento = $i",
            BeanPropertyRowMapper(Leitura::class.java)
        )
    }

    fun estado(i: Int):List<Leitura> {
        return jdbcTemplate.query("select fkEstado from GustavoEquipamento where idEquipamento = $i",
            BeanPropertyRowMapper(Leitura::class.java)
        )
    }

    fun cidade(i: Int):List<Leitura> {
        return jdbcTemplate.query("select fkCidade from GustavoEquipamento where idEquipamento = $i",
            BeanPropertyRowMapper(Leitura::class.java)
        )
    }

    fun equipamento(i: Int):List<Leitura> {
        return jdbcTemplate.query("select idEquipamento from GustavoEquipamento where fkEstado = $i",
            BeanPropertyRowMapper(Leitura::class.java)
        )
    }

    fun componente(i:String):List<Leitura> {
        return jdbcTemplate.query("select idComponente from GustavoEquipamento where nomeComponente = $i",
            BeanPropertyRowMapper(Leitura::class.java)
        )
    }
}