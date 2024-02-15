#!/usr/bin/env python3
"""Send advisory to UMB

This script will send a hello world message to UMB.
The topic and env are set as constants at the top.

Example usage:

export UMB_CERT=/path/to/crt
export UMB_KEY=/path/to/key
./send_advisory_to_umb.py

"""
import stomp
import os
import time

ENV = "dev"
UMB_TOPIC = "/topic/VirtualTopic.eng.konflux.test"

UMB_URLS = {
    "dev": "umb.dev.api.redhat.com",
    "qa": "umb.qa.api.redhat.com",
    "stage": "umb.stage.api.redhat.com",
    "prod": "umb.api.redhat.com"
}


def get_key_and_cert():
    cert_string = "UMB_CERT"
    key_string = "UMB_KEY"
    cert = os.environ.get(cert_string)
    key = os.environ.get(key_string)

    if cert is None or key is None:
        # cert + key need to be provided using env variable
        raise Exception(
            f"No auth details provided for UMB. Define {cert_string} + {key_string}"
        )
    elif not os.path.exists(cert) or not os.path.exists(key):
        raise Exception(
            f"{cert_string} or {key_string} does not point to a file that exists."
        )

    return key, cert


def main():

    # Connection parameters
    host_and_ports = [(UMB_URLS[ENV], 61612)]
    key, cert = get_key_and_cert()

    conn = stomp.Connection(host_and_ports=host_and_ports)
    conn.set_ssl(for_hosts=host_and_ports, key_file=key, cert_file=cert)

    # Connect to the STOMP broker
    conn.connect(wait=True)

    # Send a message
    conn.send(body='Hello, STOMP! Test 3!', destination=UMB_TOPIC)

    time.sleep(2)

    # Disconnect from the STOMP broker
    conn.disconnect()


if __name__ == "__main__":  # pragma: no cover
    main()
