from sqlite import get_connection


class Database:
    def execute(self, query, params=()):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query, params)

        connection.commit()
        connection.close()

    def fetch_all(self, query, params=()):
        connection = get_connection()

        connection.row_factory = lambda cursor, row: {
            col[0]: row[idx] for idx, col in enumerate(cursor.description)
        }

        cursor = connection.cursor()
        cursor.execute(query, params)

        rows = cursor.fetchall()

        connection.close()

        return rows
