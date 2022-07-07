
  
#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
Example to show receiving batch messages from a Service Bus Queue asynchronously.
"""

import os
import asyncio
from azure.servicebus.aio import ServiceBusClient
import json
from azure.servicebus import ServiceBusMessage
import sys

CONNECTION = "Endpoint=sb://chatbot-dn-dev.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=QnEHC0FxdyuKL4v/WiW9LSiyX/Hc8TMwC+T7OPyZJqI="
CONNECTION_STR = os.getenv('SERVICE_BUS_CONNECTION_STR', None) or CONNECTION
QUEUE = "stage-response"
QUEUE_NAME = os.getenv("SERVICE_BUS_QUEUE_NAME", None) or QUEUE

correct_correlation_id = sys.argv[1]
# correct_correlation_id = '196c33e7-b597-44aa-ba43-d21d547eab79'

async def main():
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR)

    async with servicebus_client:
        receiver = servicebus_client.get_queue_receiver(queue_name=QUEUE_NAME)
        async with receiver:
            received_msgs = await receiver.receive_messages(max_message_count=10, max_wait_time=5)
            if len (received_msgs) == 0: 
                print ('Não tem novas mss disponiveis')
            for msg in received_msgs:
                message = str(msg)
                current_correlation_id = json.loads(message)['correlation_id']
                print('RESPOSTA DA DANI => ', message)
                if current_correlation_id != correct_correlation_id:
                    print('Correlation id error')
                    print(current_correlation_id)
                    print(correct_correlation_id)
                    print('')
                await receiver.complete_message(msg)

asyncio.run(main())

            