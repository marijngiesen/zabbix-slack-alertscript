#!/usr/bin/python

import sys

import requests


URL = "http://192.168.0.251:8080/hubot/notify"
USERNAME = "Zabbix"
RECOVERY_EMOJI = ":troll:"
UNKNOWN_EMOJI = ":thought_balloon:"
SEVERITY_EMOJI = {
    "not classified": ":bulb:",
    "information": ":speech_balloon:",
    "warning": ":warning:",
    "average": ":rotating_light:",
    "high": ":fire:",
    "disaster": ":boom:"
}


def send_to_slack(channel, message, emoji):
    url = "%s/%s" % (URL, channel)
    payload = {"message": "%s %s" % (emoji, message)}
    requests.post(url, data=payload)
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Usage: %s <channel> <subject> <message>\n" % sys.argv[0]
        print " channel: the channel to post to (include the #)"
        print " subject: must contain PROBLEM or RECOVERY a : and severity (example: PROBLEM:average)"
        print " message: the message to post (normally this is 'TRIGGER.NAME on HOST.NAME (HOST.IP)')"
        sys.exit(1)

    channel = sys.argv[1]
    subject = sys.argv[2].split(":")[0].lower()
    severity = sys.argv[2].split(":")[1].lower()
    message = sys.argv[3]

    if "#" in channel:
        channel = channel.replace("#", "")

    if subject not in ["problem", "recovery"] or severity not in SEVERITY_EMOJI.keys():
        send_to_slack(channel, "Zabbix reports: %s" % message, UNKNOWN_EMOJI)

    if severity in ["not classified", "information"]:
        send_to_slack(channel, "Zabbix reports: %s" % message, SEVERITY_EMOJI[severity])

    if subject == "problem":
        send_to_slack(channel, "Zabbix reports a problem: %s." % message, SEVERITY_EMOJI[severity])

    if subject == "recovery":
        send_to_slack(channel, "Zabbix reports that the problem \"%s\" has been solved." % message, RECOVERY_EMOJI)
