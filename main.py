
from re import X

from kivy.lang.builder import Builder
from kivy.app import App
from kivymd.app import MDApp
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivymd import toast
from kivy.uix.screenmanager import ScreenManager, Screen
from mnemonic.mnemonic import main
from pyasn1.type.univ import Boolean
import pyrebase
from requests.models import HTTPError
import random
import binascii
import mnemonic
import bip32utils
import urllib3
from bs4 import BeautifulSoup
import time
import os
from os.path import dirname, join
import pyrebase
from kivy.clock import Clock
from urllib3.exceptions import InsecureRequestWarning   
import datetime


def show_toast(self):
        
    toast('Test Kivy Toast')

class BitcoinSeedChecking:

    output1 = ''    
    value1 = ''
    
    
         
    def generate_12_word_key():
        swordlist = ['adult', 'affair', 'alien', 'amatuer', 'animal', 'artefact', 'baby', 'balance', 'barely', 'behave', 'behind', 'benefit', 'betray', 'beyond', 'black', 'bless', 'body', 'bone', 'boss ', 'bottom ', 'bounce', 'boy', 'brother', 'business', 'call', 'chase', 'choice', 'choose', 'control', 'cream', 'curious ', 'cute', 'daughter', 'deal', 'diamond', 'dog', 'doll', 'dress', 'dream', 'drive', 'drop', 'earn', 'edge', 'empty', 'enjoy', 'exchange', 'expire', 'expose', 'exotic', 'faith', 'fantasy', 'female', 'finger', 'finish', 'firm', 'fun', 'girl', 'goddess', 'hammer', 'have', 'head', 'hole', 'horn', 'honey', 'home', 'hungry', 'hurt', 'husband', 'inmate', 'job', 'kid', 'kiss', 'lady', 'live', 'love', 'loyal', 'man', 'manage', 'marriage', 'master', 'mean', 'member', 'more', 'mother', 'obey', 'okay', 'online', 'open', 'outside', 'owner', 'paddle', 'payment', 'phone', 'picture', 'pink', 'pizza', 'play', 'please', 'plunge', 'point', 'pole', 'position', 'power', 'price', 'private', 'real', 'ready', 'remember', 'remove', 'right', 'ring', 'romance', 'rough', 'run', 'satisfy', 'scissors', 'shaft', 'sister', 'six', 'skirt', 'skin', 'sleep', 'smile', 'special', 'spoil', 'squeeze', 'submit', 'text', 'that', 'there', 'they', 'thing', 'this', 'tip', 'together', 'tongue', 'tool', 'top', 'toy', 'trust', 'truth', 'truly', 'true', 'urge', 'use', 'wait', 'want', 'warm', 'way', 'wedding', 'welcome', 'wet', 'what', 'when ', 'where', 'whip', 'wife', 'will', 'win', 'wire', 'woman', 'work', 'write', 'you']
        counter = 1
        key = []
        new_word = key.append(random.choice(swordlist))
        while counter != 12 :
            for i in key:
                new_word = str(random.choice(swordlist))
                if (i != new_word) & (counter != 12):
                    key.append(new_word)
                    counter = counter + 1
                    skey = " ".join(key)
                    
        return skey

    def bip39( skey):
        mobj = mnemonic.Mnemonic("english")
        seed = mobj.to_seed(skey)
        bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
        bip32_child_key_obj = bip32_root_key_obj.ChildKey(
            44 + bip32utils.BIP32_HARDEN
        ).ChildKey(
            0 + bip32utils.BIP32_HARDEN
        ).ChildKey(
            0 + bip32utils.BIP32_HARDEN
        ).ChildKey(0).ChildKey(0)
        
        blockchain_address = str("https://www.blockchain.com/btc/address/" + str(bip32_child_key_obj.Address()))
        http = urllib3.PoolManager()
        response = http.request('GET', blockchain_address)
        soup = BeautifulSoup(response.data.decode('utf-8'), features="lxml")
        
        value = "".join(soup.findAll("span", text=True)[34])
        value = int(value[28])
        
        
        dict1 =  {
            'mnemonic_words': skey,
            'addr': bip32_child_key_obj.Address(),
            'publickey': binascii.hexlify(bip32_child_key_obj.PublicKey()).decode(),
            'privatekey': bip32_child_key_obj.WalletImportFormat(),
            'coin': 'BTC',
            'blockchain_address': blockchain_address,
            'value': value
        }
        time.sleep(2)

        return dict1
    
    def output(dict1):
        
        output = str(
                     "Trying address: " + dict1['addr'] +
                     os.linesep +
                     os.linesep +
                     "Keys: " +
                     os.linesep +
                     os.linesep +
                     dict1['publickey'] +
                     os.linesep +
                     dict1['privatekey'] +
                     os.linesep +
                     "Seed phrase: " + dict1['mnemonic_words'] +
                     os.linesep +
                     os.linesep +
                     "Value: " + str(dict1['value']) +
                     
                     os.linesep +
                     
                     "_________________" +
                     os.linesep +
                     os.linesep +
                     "Trying again...." +
                     os.linesep +
                     "_________________" +
                     os.linesep +
                     os.linesep) 

        return output

class ScreenOne(Screen):

    isAuth = ObjectProperty()
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    auth_email = ''
    

    def getAuth(self):
        email = self.email.text
        password = self.password.text
        

        print(email, password)

        config = {

            "apiKey": "AIzaSyDwGBAjE_S_b_4ACJF2LsL9hIczljpmo2Y",
            "authDomain": "bitcoin-project-372bb.firebaseapp.com",
            "databaseURL": "https://bitcoin-project-372bb-default-rtdb.firebaseio.com",
            "storageBucket": "bitcoin-project-372bb.appspot.com",
            "serviceAccount": "C:/Users/shann/Downloads/bitcoinprojectkey.json"
        }

        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()

        try:
            auth.sign_in_with_email_and_password(email, password)
            toast.kivytoast("Logged in.")
            ScreenOne.isAuth = True
            ScreenOne.auth_email = email
            print(ScreenOne.auth_email)
            
        except HTTPError:
            toast.toast("Problem logging in...") 

            
            ScreenOne.isAuth = False
            
    def switch_screen(self, **args):

        
            
        
            

        if ScreenOne.isAuth ==True:
            
            self.manager.current = 'main'

    def sign_up(self):

        self.manager.current = 'signup'
            
class ScreenTwo(Screen):

    number = NumericProperty()
    counter = 0

    
    

    config = {

            "apiKey": 'Cant give API KEY',
            "authDomain": "bitcoin-project-372bb.firebaseapp.com",
            "databaseURL": "https://bitcoin-project-372bb-default-rtdb.firebaseio.com",
            "storageBucket": "bitcoin-project-372bb.appspot.com",
            "serviceAccount": "C:/Users/shann/Downloads/bitcoinprojectkey.json"
        }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
            
    
    
    
    def my_callback(self, dt):
        urllib3.disable_warnings(InsecureRequestWarning)
        key = BitcoinSeedChecking.generate_12_word_key()
        dict1 = BitcoinSeedChecking.bip39(key)
        output = BitcoinSeedChecking.output(dict1)
        self.ids.kvoutput.text = output
        self.counter = self.counter + 1

        email = ScreenOne.auth_email
        print(email)
        username = email.split("@")[0]
        print(self.counter)
        print(username)
        data = {'num_of_tries_this_session': self.counter}
        self.db.child("Users").child(username).update(data)
        
        
        
        total_tries_db = self.db.child("Users").child(username).get()
        print(total_tries_db)
        total_tries_db = total_tries_db.val()
        print(total_tries_db)
        total_tries_db = total_tries_db['total_tries']
        
        print(total_tries_db)

        

        total_tries = int(total_tries_db) + 1
        data1 = {'total_tries': total_tries}
        ct = datetime.datetime.now()
        data3 = {'last_session':str(ct)}

        global_tries = self.db.child("Global").get()
            
        global_tries = total_tries_db.val()
            
        global_tries = total_tries_db['Total_Tries']

        global_tries = int(global_tries) + 1

        num_tries_data = {"Num_tries" : global_tries}

        self.db.child("Global").child("Num_Tries")
        self.db.child("Global").update(num_tries_data)

        if dict1['value'] != 0:
            Clock.unschedule(self.my_callback)
            toasttoast("Hit")
            print(output)

        if HTTPError:
            toast.toast("Connection problem")

        
        
        
        
        
        self.db.child("Users").child(username).update(data1)
        self.db.child("Users").child(username).update(data3)


    def start(self):
        Clock.schedule_interval(self.my_callback, 1)
        
        
        
       
        
    def stop(self):
        Clock.unschedule(self.my_callback)
        self.manager.current = 'login'

class ScreenThree(Screen):

    email = ObjectProperty(None)
    bitcoin = ObjectProperty(None)
    password = ObjectProperty(None)
    password2 = ObjectProperty(None)

    def submit(self):
        email = self.email.text
        bitcoin = self.bitcoin.text
        password = self.password.text
        password2 = self.password2.text
        username = email.split("@")[0]
        isAuth = True

        if password != password2:
            print("passwords dont match")
        
        config = {

            "apiKey": "Cant give API key",
            "authDomain": "bitcoin-project-372bb.firebaseapp.com",
            "databaseURL": "https://bitcoin-project-372bb-default-rtdb.firebaseio.com",
            "storageBucket": "bitcoin-project-372bb.appspot.com",
            "serviceAccount": "C:/Users/shann/Downloads/bitcoinprojectkey.json"
        }

        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()

        try:
            auth.create_user_with_email_and_password(email, password)
            print("logged in")
            ScreenThree.isAuth = True
            data1 = {'bitcoin': bitcoin}
            data2 = {'email' : email}
            data3 = {'num_of_tries_this_session': '0'}
            data4 = {"total_tries" : '0'}
            ct = datetime.datetime.now()
            data5 = {"creation_date": str(ct)}
            data6 = {'last_session_date' : ''}
            

            
            db = firebase.database()
            
            db.child("Users").child(username).set(data1)
            db.child("Users").child(username).update(data2)
            db.child("Users").child(username).update(data3)
            db.child("Users").child(username).update(data4)
            db.child("Users").child(username).update(data5)
            db.child("Users").child(username).update(data6)

            num_users = db.child("Global").get()
            
            num_users = num_users.val()
            
            num_users = num_users['Num_Users']

            num_users = int(num_users) + 1

            num_users_data = {"Num_Users" : num_users}

            db.child("Global")
            db.child("Global").update(num_users_data)
            
            
            
           

            
        except HTTPError:
            print("Check connection and input.") 
            ScreenThree.isAuth = False
            
        
        

    def cancel(self):
        self.manager.current = 'login'

class MyScreenManager(ScreenManager):
    pass
        
class MyApp1(MDApp):

    


    def build(self):
        Clock.max_iteration = 20
        self.theme_cls.theme_style = "Dark"  
        self.theme_cls.primary_palette = "Orange"
        
        
        sm = MyScreenManager()
        return sm

MyApp1().run()


