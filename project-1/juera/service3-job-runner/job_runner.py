import sys
import time
from urllib.parse import parse_qs
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

import db_connector

MAILGUN_API_KEY = 'f56ff2086d8997decb79bfa63f2fab9f-30344472-efcdc351'
MAILGUN_BASE_URL = 'https://api.mailgun.net/v3/sandbox5ad71bb119694f7fa59537881ec2b628.mailgun.org'


def main():
    try:
        db = db_connector.PostgresDatabase()
        db.connect()
    except Exception as e:
        print(str(e))
        sys.exit(0)

    while True:
        try:
            none_jobs = db.get_none_jobs()

            for job in none_jobs:
                result_created, result_id = db.create_result(job[0], '')

                if result_created:
                    job_executed, message = execute_job(job)

                    if job_executed:
                        db.update_job_status(job[0])

                    db.update_result(result_id, message)

                    try:
                        upload_email = db.get_upload_email(job[3])
                        email(upload_email[0][0], message)
                    except Exception as e:
                        print(str(e))

        except Exception as e:
            print(str(e))

        time.sleep(3)


def execute_job(job):
    job_details = parse_qs(job[1])
    job_details = {
        'code': job_details['code'][0],
        'language': job_details['language'][0],
        'input': job_details['input'][0]
    }

    try:
        response = requests.post(
            url='https://api.codex.jaagrav.in',
            data=job_details
        ).json()

        if response['error'] != '':
            return True, response['error']
        else:
            return True, response['output']
    except:
        return False, 'error for connecting to Codex'


def email(address, message):
    url = MAILGUN_BASE_URL + '/messages'
    payload = {
        'from': 'zandiyeh1379@gmail.com',
        'to': address,
        'subject': 'your code output',
        'text': message
    }

    try:
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        requests.post(url=url, data=payload)
        print(f"email sent to {address} with message: {message}")
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('job runner interrupted')
        sys.exit(0)
