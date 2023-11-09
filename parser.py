import re
import pandas as pd


def parseMessage(message, section):
    date = message[0:10]
    time = message[11:16]
    i = 19
    while message[i] != ':':
        i += 1
    sender = message[19:i]
    text = message[i + 1:len(message)]
    if '<' in text and '>' in text:
        text = text[:text.find('<')] + text[text.find('>') + 1:]
    return [date, time, sender, text, section]


def toDataFrame(file, section):
    f = open(file, "r")
    chat = f.read()
    messages = []
    first_index = 0
    for i in range(1, len(chat)):
        if re.search('\d\d-\d\d-\d{4} \d\d:\d\d', chat[i:i + 16]):
            second_index = i
            messages.append(chat[first_index:second_index - 1])
            first_index = second_index
    filteredMessages = filter(lambda msg: ':' in msg[14:], messages)
    parsedMessages = [parseMessage(msg, section) for msg in filteredMessages]
    parsedMessages = list(filter(lambda message: message[3] and not message[3].isspace(), parsedMessages))
    return pd.DataFrame(parsedMessages, columns=["Date", "Time", "Sender", "Message", "Section"])


if __name__ == '__main__':
    df_gen = toDataFrame("/home/julius/Downloads/WhatsApp-chat met General - ESN VALENCIA.txt", "General")
    df_volley = toDataFrame("/home/julius/Downloads/WhatsApp-chat met Volleyball.txt", "Volleyball")
    df_running = toDataFrame("/home/julius/Downloads/WhatsApp-chat met Running.txt", "Running")
    df_football = toDataFrame("/home/julius/Downloads/WhatsApp-chat met Football.txt", "Football")
    full_df = pd.concat([df_gen, df_volley, df_running, df_football])