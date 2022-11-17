package app

import com.github.britooo.looca.api.core.Looca
import configuracao.Conexao
import configuracao.ConexaoMySQL
import dominio.Leitura
import org.springframework.jdbc.core.JdbcTemplate
import repositorio.LeituraRepositorio
import java.sql.Connection
import java.text.DecimalFormat
import java.time.*
import java.util.*
import kotlin.concurrent.schedule
import kotlin.math.roundToInt

open class Main {
    companion object {
        @JvmStatic
        fun main(args: Array<String>) {
            println("Iniciando Conexão com banco de dados.")
            val jdbcTemplate = Conexao().getJdbcTemplate()
            println("Conexão com banco de dados SQL Server realizada com sucesso.")
            val jdbcTemplateMySQL = ConexaoMySQL().getJdbcTemplateMySQL()
            println("Conexão com banco de dados MySQL realizada com sucesso.")

            val looca = Looca()

            registrar(3, 0, jdbcTemplate, jdbcTemplateMySQL, looca)
        }

        private fun registrar(
            repeticoes: Int,
            realizada: Int,
            jdbcTemplate: JdbcTemplate,
            jdbcTemplateMySQL: Connection,
            looca: Looca
        ) {
            if (realizada < repeticoes) {
                val repositorioLeitura = LeituraRepositorio(jdbcTemplate, jdbcTemplateMySQL)
                println("Iniciando captura de dados.")

                for (i in 1..27) {
                    val percentualCPU = looca.processador
                    val percentualUso = (percentualCPU.uso * 100).roundToInt().toDouble() / 100

                    val df = DecimalFormat("#.##")
                    val percentual: Double = java.lang.Double.valueOf(percentualUso).toDouble()
                    val novaLeitura = Leitura(1, i, i, i, 1, percentual, LocalDate.now())

                    repositorioLeitura.inserir(novaLeitura)

                    println(
                        "SQL Server - Inserindo dados de CPU, Equipamento: $i, percentual $percentual% - Data: ${
                            LocalDate.now()
                        }"
                    )

                    println(
                        "MySQL - Inserindo dados de CPU, Equipamento: $i, percentual $percentual% - Data: ${
                            LocalDate.now()
                        }"
                    )

                    Thread.sleep(2_000)
                }
            }

            Timer().schedule(3000) {
                registrar(repeticoes, realizada + 1, jdbcTemplate, jdbcTemplateMySQL, looca)
            }
        }
    }
}
