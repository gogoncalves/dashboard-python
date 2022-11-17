package configuracao

import java.sql.Connection
import java.sql.DriverManager

class ConexaoMySQL {

    fun getJdbcTemplateMySQL(): Connection {

        Class.forName("com.mysql.cj.jdbc.Driver")

        return DriverManager.getConnection(
            "jdbc:" + "mysql" + "://" + "127.0.0.2" + ":" + "3305" + "/" + "dashboard",
            "root", "root")
    }
}