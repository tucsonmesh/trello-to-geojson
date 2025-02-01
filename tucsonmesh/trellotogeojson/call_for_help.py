"""Simple CLI for sending notifications to a Slack channel"""

import argparse
import logging
import os
import sys

# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")


def call_for_help():
    """Send a Slack message to a channel"""

    # Parse command-line arguments
    # See https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(
        prog="call-for-help",
        description="Send a Slack message to a channel",
        usage="%(prog)s channel_id message"
    )
    parser.add_argument(
        "channel_id",
        help="Channel ID where message will be sent"
    )
    parser.add_argument(
        "message",
        help="Message contents to send"
    )

    args = parser.parse_args()

    if SLACK_BOT_TOKEN is None:
        logging.error("You must specify a SLACK_BOT_TOKEN environment variable.")
        sys.exit(1)

    # WebClient instantiates a client that can call API methods
    # When using Bolt, you can use either `app.client` or the `client` passed to listeners.
    client = WebClient(token=SLACK_BOT_TOKEN)

    try:
        # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel=args.channel_id, 
            text=args.message,
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")
        sys.exit(1)


if __name__ == "__main__":
    call_for_help()
