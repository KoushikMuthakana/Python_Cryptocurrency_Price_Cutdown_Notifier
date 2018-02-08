import json
from twilio.rest import Client
import yagmail
import requests as req


def getCredentials() -> dict:
    '''
    Parameters: None

    Fetches Gmail and Twilio Credentials form text file

    :return:Credentials
    '''
    _cred = dict()
    with open(r"D:\Credentials.txt", 'r') as fp:
        return json.loads(fp.read())


def getCoinsPrices() -> dict:
    '''
    Uses the Coinmarketcap API to fetch the top 10 cryptocurrency prices

    :return Bitcoin,Ripple, Cardano Prices:
    '''
    _coins_cost_dict = dict()
    responseData = req.get("https://api.coinmarketcap.com/v1/ticker/?convert=INR&limit=10")
    coinsCostjson_Data = json.loads(responseData.content.decode('utf-8'))
    for data in coinsCostjson_Data:
        if data.get('name') == 'Bitcoin':
            _coins_cost_dict['Bitcoin'] = float(data.get('price_inr'))
        elif data.get('name') == 'Ripple':
            _coins_cost_dict['Ripple'] = float(data.get('price_inr'))
        elif data.get('name') == 'Cardano':
            _coins_cost_dict['Cardano'] = float(data.get('price_inr'))
    return _coins_cost_dict


def email_notification(coins_cost_dict: dict, cred: dict) -> None:
    '''
    :param coins_cost_dict: latest CryptoCurrency Costs
    :param cred: Gmail and Twilio Credentials
    :return: None

    Sends Emails to the target people
    '''
    _msg = '''
          Ripple/Cardano price ,                       
          Current Ripple Price: RS {0}
          Current Cardano Price:RS {1}
          '''.format(coins_cost_dict.get("Ripple"), coins_cost_dict.get("Cardano"))
    _targets = ['target1@gmail.com', 'target2@gmail.com', 'target3@gmail.com']
    _subject = 'Alert::Crytptocurrency News'
    mail = yagmail.SMTP(cred['Gmail']['UserID'], cred['Gmail']['Password'])
    mail.send(_targets, _subject, _msg)
    print("Email has Sent Successfully ..!!")


def message_Notification(coins_cost_dict: dict, cred: dict) -> None:
    '''
    :param coins_cost_dict: latest CryptoCurrency Costs
    :param cred: Gmail and Twilio Credentials
    :return:None
    Sends SMS Notifications to target mobiles Numbers
    '''
    _twilioClient = Client(cred['Twilio']['twilioAccID'], cred['Twilio']['twilioAuthToken'])
    _myNumber = "+1999999999"
    _clientNumber = "+919991929292"
    _msg = "Ripple: RS {0} / Cardano : RS {1} Price Fall Down".format(coins_cost_dict.get("Ripple"),
                                                                      coins_cost_dict.get("Cardano"))
    _twilioClient.messages.create(body=_msg, from_=_myNumber, to=_clientNumber)
    print('Message Send Successfully..!!')


if __name__ == '__main__':
    _coins = getCoinsPrices()
    _cred = getCredentials()
    _XRPPurchased = 98.00
    _ADAPurchased = 32.00
    '''
    If Prices cut down to 50% of purchased price, get a Mail and SMS Notification
    '''
    if _coins.get('Ripple') <= (_XRPPurchased * 50 / 100) or _coins.get('Cardano') <= (_ADAPurchased * 50 / 100):
        email_notification(_coins, _cred)
        message_Notification(_coins, _cred)
    else:
        print('*********')