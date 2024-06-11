import os

from openai import OpenAI

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],
)

message_1 = """Nabycie prawa do urlopu wypoczynkowego
Prawo do pierwszego urlopu wypoczynkowego pracownik podejmujący pracę po raz pierwszy, uzyskuje z upływem każdego miesiąca pracy, w wymiarze 1/12 wymiaru urlopu przysługującego mu po przepracowaniu roku. Za każdy miesiąc ma prawo do 1/12 z 20 dni (czyli 1,66 dnia) – tj. nabywa się prawo do urlopu z dołu.

Prawo do kolejnych urlopów nabywa się w każdym następnym roku kalendarzowym – tj. nabywa się prawo do urlopu z góry.

W razie ustania stosunku pracy i nawiązania w trakcie roku kalendarzowego wymiar urlopu ustala się proporcjonalnie do okresu przepracowanego u danego pracodawcy. W takim przypadku 1 miesiąc odpowiada 1/12 wymiaru urlopu wypoczynkowego. Niepełny kalendarzowy miesiąc pracy zaokrągla się w górę do pełnego miesiąca. Dotyczy to także uprawnienia do kolejnego urlopu w przypadku zatrudnienia w trakcie roku kalendarzowego.

Niepełny dzień urlopu zaokrągla się w górę do pełnego dnia."""

message_2 = """Wymiar urlopu wypoczynkowego
Wymiar urlopu zależy od ogólnego stażu pracy – czyli wszystkich okresów zatrudnienia. Wynosi on:

20 dni przy okresie zatrudnienia krótszym niż 10 lat,
26 dni przy okresie zatrudnienia wynoszącym co najmniej 10 lat.
Przy zatrudnieniu w niepełnym wymiarze czasu pracy wymiar urlopu ustala się proporcjonalnie do wymiaru zatrudnienia np. przy ½ etatu jest to 10 lub 13 dni.

Do okresu zatrudnienia, od którego zależy wymiar urlopu wlicza się okresy poprzedniego zatrudnienia bez względu na przerwy w zatrudnieniu oraz sposób ustania stosunku pracy.

Wlicza się również okresy zakończonej nauki:

zasadniczej lub innej równorzędnej szkoły zawodowej - przewidziany programem nauczania czas trwania nauki, nie więcej jednak niż 3 lata,
średniej szkoły zawodowej - przewidziany programem nauczania czas trwania nauki, nie więcej jednak niż 5 lat,
średniej szkoły zawodowej dla absolwentów zasadniczych (równorzędnych) szkół zawodowych - 5 lat,
średniej szkoły ogólnokształcącej - 4 lata,
szkoły policealnej - 6 lat,
szkoły wyższej - 8 lat.
Okresy nauki nie podlegają sumowaniu.

Jeżeli pracownik pobierał naukę w czasie zatrudnienia, do okresu pracy, od którego zależy wymiar urlopu, wlicza się bądź okres zatrudnienia, w którym była pobierana nauka, bądź okres nauki, zależnie od tego, co jest korzystniejsze dla pracownika."""

message_3 = """Udzielanie urlopu wypoczynkowego
Urlop powinien być udzielony w tym roku, w którym pracownik nabył do niego prawo. Urlop powinien być udzielony zgodnie z planem urlopów. Plan urlopów ustala pracodawca, biorąc pod uwagę wnioski pracowników i konieczność zapewnienia normalnego toku pracy. W braku takiego planu następuje to na podstawie porozumienia pracownika z pracodawcą.

Pracownik może wykorzystać 4 dni urlopu na swój wniosek, który pracodawca uwzględnia (tzw. „urlop na żądanie”).

Urlop może być wykorzystany w częściach na wniosek pracownika przy czym jedna część ma obejmować co najmniej 14 kolejnych dni kalendarzowych.

Pracodawca może jednostronnie udzielić urlopu pracownikowi w okresie wypowiedzenia.

Na wniosek pracownicy udziela się jej urlopu bezpośrednio po urlopie macierzyńskim (rodzicielskim).  Dotyczy to także pracownika-ojca wychowującego dziecko, który korzysta z urlopu macierzyńskiego, rodzicielskiego lub ojcowskiego. Pracodawca ma w takiej sytuacji obowiązek udzielenia urlopu wypoczynkowego.

W razie niewykorzystania urlopu w roku kalendarzowym udziela się go do 30 września następnego roku.

Urlopu udziela się w dni, które są dla pracownika dniami pracy, zgodnie z obowiązującym go rozkładem czasu pracy, w wymiarze godzinowym, odpowiadającym dobowemu wymiarowi czasu pracy pracownika w danym dniu.

Przy udzielaniu urlopu jeden dzień urlopu odpowiada 8 godzinom pracy (20 dni x 8 godzin = 160 godzin; 26 dni x 8 godzin = 208 godzin).

Gdy pracownika obowiązuje niższa dobowa norma czasu pracy jego dzień urlopu odpowiada tej niższej normie (np. 7 godzin w przypadku pracownika niepełnosprawnego – 20 dni x 7 godzin = 140 godzin; 26 dni x 7 godzin = 182 godziny)."""

def preprocess_messages(messegas):
    preprocessed_messages = [{'role':message['sender'], 'content':message['message']} for message in messegas]
    if preprocessed_messages[0]['role'] != 'system':
        preprocessed_messages.insert(0, {'role':'system', 'content': 'You are a semantic parser. Your job is to write a list of user needs based on the context it provides.'})
    return preprocessed_messages

def call_openai(messages, context):
    if context:
        messages.append({'role':'system','content':context})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        temperature=1,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        response = response.choices[0].message.content
    except:
        response = "**error - no response from openai**"
    return response

if __name__ == '__main__':
    messages = [{'sender': 'User', 'message': 'Hello! I will have seminar session at my university next week. I will present the topic of cancer treatment in cats. Could you help me with preparing to this task?'}]
    r = preprocess_messages(messages)
    print(r)