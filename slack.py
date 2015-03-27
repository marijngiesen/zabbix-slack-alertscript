import sys
import json
import requests

URL = "https://hooks.slack.com/services/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"
USERNAME = "Zabbix"
RECOVERY_EMOJI = ":troll:"
UNKNOWN_EMOJI = ":thought_balloon:"
SEVERITIES = {
    "not classified": ":bulb:",
    "information": ":speech_balloon:",
    "warning": ":warning:",
    "average": ":rotating_light:",
    "high": ":fire:",
    "disaster": ":boom:"
}


def send_to_slack(channel, message, emoji):
    payload = {
        "channel": channel,
        "username": USERNAME,
        "text": message,
        "icon_emoji": emoji,
    }

    requests.post(URL, json=payload)
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Usage: %s <channel> <subject> <message>\n" % sys.argv[0]
        print " channel: the channel to post to (include the #)"
        print " subject: must contain PROBLEM or RECOVERY a : and severity (example: PROBLEM:average)"
        print " message: the message to post (normally this is 'TRIGGER.NAME on HOST.NAME (HOST.IP)')"
        sys.exit(1)

    channel = sys.argv[1]
    subject = sys.argv[2].split(":")[0]
    severity = sys.argv[2].split(":")[1]
    message = "%s: %s" % (subject, sys.argv[3])

    if "#" not in channel:
        channel = "#%s" % channel

    if subject.lower() not in ["problem", "recovery"] or severity not in SEVERITIES.keys():
        send_to_slack(channel, message, UNKNOWN_EMOJI)

    if subject.lower() == "problem":
        emoji = SEVERITIES[severity]
    elif subject.lower == "recovery":
        emoji = RECOVERY_EMOJI

    send_to_slack(channel, message, emoji)


