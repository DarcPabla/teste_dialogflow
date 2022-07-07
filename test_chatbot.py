#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
Example to show receiving batch messages from a Service Bus Queue asynchronously.
"""

import codecs
import sys
import os
import asyncio
from typing import List, Optional
from uuid import uuid4
from azure.servicebus.aio import ServiceBusClient
import json
from azure.servicebus import ServiceBusMessage

os.system("")

CONNECTION = "Endpoint=sb://chatbot-dn-dev.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=QnEHC0FxdyuKL4v/WiW9LSiyX/Hc8TMwC+T7OPyZJqI="
CONNECTION_STR = os.getenv("SERVICE_BUS_CONNECTION_STR", None) or CONNECTION
RECEIVER_QUEUE = "stage-response"
RECEIVER_QUEUE_NAME = (
    os.getenv("SERVICE_BUS_RECEIVER_QUEUE_NAME", None) or RECEIVER_QUEUE
)
SENDER_QUEUE = "stage-request"
SENDER_QUEUE_NAME = os.getenv("SERVICE_BUS_SENDER_QUEUE_NAME", None) or SENDER_QUEUE


def create_message(user_message: str, session_id: str, correlation_id: str):
    return ServiceBusMessage(
        json.dumps(
            {
                "action": "message_request_bot",
                "payload": {
                    "agent_id": "27b5dd19-c3fd-481b-a913-c609045abe47",
                    "session_id": session_id,
                    "text": user_message,
                    "language_code": "pt-br",
                },
                "correlation_id": correlation_id,
            }
        )
    )


class ConverstaionReport:
    passed: bool
    logs: List[object]
    expected_correlation_id: Optional[str]
    wrong_message: Optional[object]

    def __init__(
        self,
        passed: bool,
        logs: List[object],
        expected_correlation_id: Optional[str] = None,
        wrong_message: Optional[object] = None,
    ) -> None:
        self.passed = passed
        self.logs = logs
        self.expected_correlation_id = expected_correlation_id
        self.wrong_message = wrong_message


async def execute_conversation(
    user_messages: List[str], verbose: bool = False
) -> ConverstaionReport:
    logs = []
    client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR)
    async with client:
        session_id = str(uuid4())

        sender = client.get_queue_sender(queue_name=SENDER_QUEUE_NAME)
        receiver = client.get_queue_receiver(queue_name=RECEIVER_QUEUE_NAME)

        async with sender, receiver:
            # Remove old messages from the receiver queue
            received_messages = await receiver.receive_messages(
                max_message_count=100, max_wait_time=5
            )
            for message in received_messages:
                await receiver.complete_message(message)

            # Start conversation with the bot
            for user_message in user_messages:
                correlation_id = str(uuid4())
                message = create_message(user_message, session_id, correlation_id)
                await sender.send_messages(message)

                if verbose:
                    print(f'Sent message "{user_message}"')
                log = {
                    "sender": "user",
                    "message": user_message,
                    "correlation_id": correlation_id,
                }
                logs.append(log)

                # Read bot answers.
                received_messages = await receiver.receive_messages(max_wait_time=5)
                for message in received_messages:
                    response = json.loads(str(message))
                    await receiver.complete_message(message)

                    if verbose:
                        print(f'Received message "{response["message"]}"')
                    log = {"sender": "bot", **response}
                    logs.append(log)

                    if response["correlation_id"] != correlation_id:
                        return ConverstaionReport(
                            passed=False,
                            logs=logs,
                            expected_correlation_id=correlation_id,
                        )

        return ConverstaionReport(passed=True, logs=logs)


class Test:
    name: str
    user_messages: List[str]

    def __init__(self, name: str, user_messages: List[str]) -> None:
        self.name = name
        self.user_messages = user_messages


# https://stackoverflow.com/a/54955094
class style:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"


async def main():
    tests: List[Test] = [
        Test(
            name="fluxo_1_feliz_leitora",
            user_messages=["Oi", "Leitora", "Sim", "ATM voltou a funcionar", "Não"],
        ),
        Test(
            name="fluxo_2_perguntas",
            user_messages=["Oi", "Leitora", "Sim", "ATM voltou a funcionar", "Sim"],
        ),
        Test(
            name="fluxo_3_palavra_trocada",
            user_messages=[
                "Oi",
                "Leitora",
                "Sim",
                "ATM ainda não operante",
                "Não",
                "Não",
            ],
        ),
        Test(
            name="fluxo_4_nao_operante",
            user_messages=[
                "Oi",
                "Leitora",
                "Sim",
                "ATM ainda não operante",
                "ATM ainda não operante",
                "Não",
            ],
        ),
        Test(
            name="fluxo_5_nao_operante",
            user_messages=[
                "Oi",
                "Leitora",
                "Sim",
                "ATM ainda não operante",
                "ATM ainda não operante",
                "Sim",
            ],
        ),
        Test(
            name="fluxo_6_nenhuma_das_alternativas",
            user_messages=["Oi", "Leitora", "Não", "Não"],
        ),
        Test(
            name="fluxo_7_nda_sem_finalizar",
            user_messages=["Oi", "Leitora", "Não", "Sim"],
        ),
    ]

    for test in tests:
        result = await execute_conversation(user_messages=test.user_messages)

        print(f'Test "{test.name}"', end=" ")
        print(f"{style.GREEN}passed" if result.passed else f"{style.RED}failed")
        print(style.RESET, end="")

        with codecs.open(f"./test-logs/{test.name}.json", "w", encoding="utf-8") as f:
            json.dump(result.logs, f, ensure_ascii=False, indent=2)


asyncio.run(main())
