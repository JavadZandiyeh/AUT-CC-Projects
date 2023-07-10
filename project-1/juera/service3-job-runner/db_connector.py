import datetime

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

    def insert(self, query: str, vals: tuple) -> tuple:
        try:
            self.cursor.execute(query, vals)
            self.cursor.execute('SELECT LASTVAL()')
            self.connection.commit()
            return True, self.cursor.fetchone()[0]
        except Exception as e:
            print(str(e))
            return False, None

    def update(self, query: str, vals: tuple) -> bool:
        try:
            self.cursor.execute(query, vals)
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_none_jobs(self):
        return self.select("select * from juera_app_job where status = 'none'")

    def update_job_status(self, job_id):
        query = "update juera_app_job set status = 'executed' where id = %s"
        vals = (job_id,)
        return self.update(query, vals)

    def get_upload_email(self, file_id: int) -> list:
        return self.select(f"select email from juera_app_upload where id={file_id}")

    def create_result(self, job_id, output):
        query = "insert into juera_app_result (job_id, output, status, executed_date) values (%s, %s, %s, %s)"
        vals = (job_id, output, 'in_progress', datetime.datetime.now())
        return self.insert(query, vals)

    def update_result(self, result_id, output):
        query = "update juera_app_result set (status, output) = ('done', %s) where id = %s"
        vals = (output, result_id)
        return self.update(query, vals)
