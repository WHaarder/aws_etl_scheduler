from json import dumps

from util.db import db_connect

from sqlalchemy import create_engine
from urllib.parse import quote_plus

import boto3
import base64
from botocore.exceptions import ClientError


def get_secret():

    secret_name = ""
    region_name = ""

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            raise e
        elif e.response["Error"]["Code"] == "AccessDeniedException":
            raise e
    else:
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
        else:
            secret = base64.b64decode(get_secret_value_response["SecretBinary"])
    return eval(secret)


def db_connect():
    secret = get_secret()
    pw = quote_plus(secret["password"])
    eng = create_engine(
        f"postgresql+psycopg2://{secret['username']}:{pw}@{secret['host']}"
    )
    conn = eng.connect()
    test = eng.execute(
        """SELECT *
            FROM pg_catalog.pg_tables;
            """
    ).fetchall()
    print(test)
    conn.close()


print("hello")


def main(event, context):
    db_connect()
    if event.get("test") == "":
        payload = {"User error": "'image' in body contains empty string."}
        status_code = 400

    else:
        try:
            print(event.get("test"))
            payload = {"Input read": event.get("test")}
            status_code = 200
        except Exception as e:
            print(e)
            payload = {"User error": "Could not predict on provided image."}
            status_code = 400

    return {"statusCode": status_code, "body": dumps(payload, allow_nan=False)}


if __name__ == "__main__":
    main("t", "t")
