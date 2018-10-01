from __future__ import print_function
import tweepy
import json
import mysql.connector
from bdateutil import parser

HASHTAGS = ['#openbanking', '#apifirst', '#devops', '#cloudfirst', '#microservices', '#apigateway', '#oauth', '#swagger', '#raml', '#openapis']

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = "634328974-"
ACCESS_TOKEN_SECRET = ""

HOST = "localhost"
USER = ""
PASSWD = ""
DATABASE = ""

# Armazena os Tweets no MySQL.
def store_data(tweeted_at, happening, username, tweet_id):
    db = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8")
    cursor = db.cursor()
    insert_query = "INSERT INTO twitter (tweet_id, username, tweeted_at, happening) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (tweet_id, username, tweeted_at, happening))
    db.commit()
    cursor.close()
    db.close()
    return


class StreamListener(tweepy.StreamListener):
    # Classe do Tweepy para acessar a API do Twitter.

    def on_connect(self):
        # Conectando a API do Twitter.
        print("Uhull conectado a API do Twitter com sucesso")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('Xiii, melhor dar uma olhada nesse erro: ' + repr(status_code))
        return False

    def on_data(self, data):
        # Conecta no MySQL para armazenar os Tweets.
            # Decodificando o JSON do Twitter
            datajson = json.loads(data)

            # Pegue os dados desejados do Tweet.
            happening = datajson['text']
            username = datajson['user']['screen_name']
            tweet_id = datajson['id']
            tweeted_at = parser.parse(datajson['created_at']) 

            # Imprimir mensagem do Tweet armazenado.
            print("Tweet armazenado em " + str(tweeted_at))

            # Insert no MySQL.
            store_data(tweeted_at, happening, username, tweet_id)

        except Exception as e:
            print(e)


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Quando 'wait_on_rate_limit=True' é necessário para ajudar na limitação da taxa da API do Twitter.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))

streamer = tweepy.Stream(auth=auth, listener=listener)
print("Rastreamento: " + str(HASHTAGS))
streamer.filter(track=HASHTAGS)
