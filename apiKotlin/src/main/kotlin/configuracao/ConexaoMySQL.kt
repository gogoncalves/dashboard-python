package configuracao

import java.sql.Connection
import java.sql.DriverManager

class ConexaoMySQL {
    val driver = Class.forName("com.mysql.cj.jdbc.Driver")

    fun getJdbcTemplateMySQL(): Connection {
        val conexao = DriverManager.getConnection("jdbc:mysql://172.17.0.2:3305/dashboard", "root", "root")

        return conexao
    }
}