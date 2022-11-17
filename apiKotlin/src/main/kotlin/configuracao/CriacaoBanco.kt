package configuracao

fun main() {

    val jdbcTemplate = Conexao().getJdbcTemplate()

    jdbcTemplate.execute("""
        create table sistema_operacional (
        id int primary key,
        nome varchar(50) not null
        );
    """)
}

