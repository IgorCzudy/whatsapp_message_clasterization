import re
import pandas as pd


def parseMessage(message, section, lang):
    date = message[0:10]
    if lang == "PL":
        date = date.replace('.', '-')
        time = message[12:17]
        i = 20
    else:
        time = message[11:16]
        i = 19
    while message[i] != ':':
        i += 1
    sender = message[19:i]
    text = message[i + 1:len(message)]
    if '<' in text and '>' in text:
        text = text[:text.find('<')] + text[text.find('>') + 1:]
    return [date, time, sender, text, section]


def toDataFrame(file, section, lang):
    f = open(file, "r")
    chat = f.read()
    messages = []
    first_index = 0
    if lang == "PL":
        for i in range(1, len(chat)):
            if re.search('\d\d.\d\d.\d{4}, \d\d:\d\d', chat[i:i + 17]):
                second_index = i
                messages.append(chat[first_index:second_index - 1])
                first_index = second_index
    else:
        for i in range(1, len(chat)):
            if re.search('\d\d-\d\d-\d{4} \d\d:\d\d', chat[i:i + 16]):
                second_index = i
                messages.append(chat[first_index:second_index - 1])
                first_index = second_index
    filteredMessages = filter(lambda msg: ':' in msg[15:], messages)
    parsedMessages = [parseMessage(msg, section, lang) for msg in filteredMessages]
    parsedMessages = list(filter(lambda message: message[3] and not message[3].isspace(), parsedMessages))
    return pd.DataFrame(parsedMessages, columns=["Date", "Time", "Sender", "Message", "Section"])


if __name__ == '__main__':
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    df_gen = toDataFrame("/home/julius/Downloads/WhatsApp-chat met General - ESN VALENCIA.txt", "General", "NL")
    df_volley = toDataFrame("/home/julius/Downloads/WhatsApp-chat met Volleyball.txt", "Volleyball", "NL")
    df_running = toDataFrame("/home/julius/Downloads/WhatsApp-chat met Running.txt", "Running", "NL")
    df_football = toDataFrame("/home/julius/Downloads/WhatsApp-chat met Football.txt", "Football", "NL")
    df_party = toDataFrame("/home/julius/Downloads/Czat WhatsApp z Party .txt", "Party", "PL")
    df_qa = toDataFrame("/home/julius/Downloads/Czat WhatsApp z UPV Q&A.txt", "Q&A", "PL")
    df_surf = toDataFrame("/home/julius/Downloads/Czat WhatsApp z Surfing.txt", "Surfing", "PL")
    df_music = toDataFrame("/home/julius/Downloads/Czat WhatsApp z Music and Jam.txt", "Music", "PL")
    full_df = pd.concat([df_gen, df_volley, df_running, df_football, df_party, df_qa, df_surf, df_music])
    print(full_df.to_string())