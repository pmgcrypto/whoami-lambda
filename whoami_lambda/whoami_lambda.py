import boto3
import json
import socket
import re
import os
import requests
from botocore.exceptions import ClientError


def get_secret():

    secret_name = os.environ.get("SECRET_ARN")

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager'
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret = eval(get_secret_value_response['SecretString'])
    return secret


def whoami_gather_info(event, context):
    open_ports = []
    closed_ports = []
    # Ports to scan.
    ports = [21, 22, 23, 25, 80,
             110, 135, 139, 143,
             443, 445, 993, 995,
             3306, 3389, 5900, 8080]

    # Get the User-Agent from the "event" dict.
    user_agent = event['multiValueHeaders']['User-Agent'][0]

    # Get the Source IP from the "event" dict.
    source_ip = event['requestContext']['identity']['sourceIp']

    # Port scan. Scan the Source IP for the items in "ports".
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((source_ip, port))
            s.close()
            open_ports.append(port)
        except:
            closed_ports.append(port)

    # Make call to IPStack to get Geographic Information
    call = requests.get(
        "http://api.ipstack.com/{}?access_key={}".format(
            source_ip,
            get_secret()['ipstack']
        )
    )
    data = call.json()

    # Check if source is ip originates from a Tor exit node.
    tor_data = requests.get("https://check.torproject.org/exit-addresses")
    tor_regex = re.findall(
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
        tor_data.text)
    if source_ip in tor_regex:
        torbool = True
    else:
        torbool = False

    # Get ISP
    isp_request = requests.get(
        "https://api.hackertarget.com/aslookup/?q={}".format(source_ip)).text
    isp = eval(isp_request)[3]

    try:
        referrer = event["multiValueHeaders"]["referrer"][0]
    except KeyError:
        referrer = "Unknown"

    response = {
        'UserAgent':    user_agent,
        'IPAddress':    source_ip,
        'ISP':          isp,
        "Referrer":     referrer,
        'IsTor':       torbool,
        'OpenPorts':   open_ports,
        'ClosedPorts': closed_ports,
        'GeographicInformation': {
            "Continent":    data["continent_name"],
            "Country":      data['country_name'],
            "Region":       data["region_name"],
            "City":         data['city']
        }
    }

    return {
        'statusCode':   200,
        'headers':  {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
        },
        'body':         json.dumps(response)
    }
