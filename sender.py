from azure.servicebus import ServiceBusClient, ServiceBusMessage
import json
from uuid import uuid4

connstr = "Endpoint=sb://chatbot-dn-dev.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=QnEHC0FxdyuKL4v/WiW9LSiyX/Hc8TMwC+T7OPyZJqI="
queue_name = "stage-request"

message = input("Message: ")

data = {
    "action":"message_request_bot",  #finish_call
    "payload":{
        "agent_id":"27b5dd19-c3fd-481b-a913-c609045abe47",
        "session_id":"49ac0faa-13c2-4a3f-8d5f-4f7a4560fd28", #inciar uma conversa, tem que mudar id
        "text": message,
        "language_code":"pt-br"
        },
    "correlation_id":"bb79e213-f854-4e56-9886-405d36fb7543"
    }


with ServiceBusClient.from_connection_string(connstr) as client:
    with client.get_queue_sender(queue_name) as sender:
        # Sending a single message
        single_message = ServiceBusMessage(json.dumps(data))
        sender.send_messages(single_message)
