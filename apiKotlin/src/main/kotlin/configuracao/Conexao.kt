package configuracao

import org.apache.commons.dbcp2.BasicDataSource
import org.springframework.jdbc.core.JdbcTemplate

class Conexao {
    val driverClassName = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    val url = "jdbc:sqlserver://healthsystem.database.windows.net;database=healthsystem;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;"
    val username = "grupo01sis"
    val password = "#GfHealthSystem01"

    fun getJdbcTemplate(): JdbcTemplate {
        val dataSource = BasicDataSource()
        dataSource.driverClassName = driverClassName
        dataSource.url = url
        dataSource.username = username
        dataSource.password = password

        val jdbcTemplate = JdbcTemplate(dataSource)
        return jdbcTemplate
    }
}