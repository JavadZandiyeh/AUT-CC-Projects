import psycopg2


class PostgresDatabase:
    def __init__(self) -> None:
        self.cursor = None
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(
            database='juera',
            user='root',
            password='umh9auXgPCxLwMDZVA7xIm0m',
            host='esme.iran.liara.ir',
            port='30476'
        )

        self.cursor = self.connection.cursor()

    def disconnect(self) -> None:
        self.cursor.close()
        self.connection.close()

    def select(self, query: str) -> list:
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert(self, query: str, vals: tuple) -> bool:
        try:
            self.cursor.execute(query, vals)
            self.connection.commit()
            return True
        except:
            return False

    def get_upload(self, file_id: int) -> list:
        return self.select(f"select * from juera_app_upload where id={file_id}")

    def create_job(self, file_id: int, job: str):
        query = "insert into juera_app_job (upload_id, job, status) values (%s, %s, %s)"
        vals = (file_id, job, 'none')
        return self.insert(query, vals)
