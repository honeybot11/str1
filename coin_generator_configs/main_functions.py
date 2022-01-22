from time import time
from json import load
from random import choice
from threading import Thread
from tabulate import tabulate
from .library import aminoboi
from . import menu_configs, autoreg_functions
from concurrent.futures import ThreadPoolExecutor

accounts = [ ]
with open("accounts.json") as data:
	accounts_list = load(data)
	for account in accounts_list:
		accounts.append(account)

		# -- coin generator functions --
		
def auth(email: str, password: str, client: aminoboi.Client):
	try:
		print(f">> deviceID -- {client.device_Id}")
		client.auth(email=email, password=password)
		print(f">> Logged in {email}...")
	except Exception as e:
		print(f">> Error in Auth {e}")
        
def coin_generator():
	send_active_object = {"start": int(time()), "end": int(time()) +300}
	return send_active_object

def generator_main_process(ndc_id: int, email: str, client: aminoboi.Client):
	timers = [coin_generator() for _ in range(50)]
	client.send_active_object(ndc_id=ndc_id, timers=timers)
	print(f">> Generating coins in {email}...")

def generating_process(ndc_id: int, email: str, client: aminoboi.Client):
	Thread(target=generator_main_process, args=(ndc_id, email, client)).start()
	
def play_lottery(ndc_id: int, client: aminoboi.Client):
	try:
		lottery = client.lottery(ndc_id=ndc_id)
		print(f">> Lottery - {lottery['api:message']}")
	except Exception as e:
		print(f">> Error in play lottery - {e}")
		
def watch_ad(client: aminoboi.Client):
	try:
		watch_ad = client.watch_ad()
		print(f">> Watch Ad - {watch_ad['api:message']}")
	except Exception as e:
		print(f">> Error in watch ad - {e}")
		
		# -- transfer coins and main function for generating coins -- 

def get_tapjoy_reward(client: aminoboi.Client):
	try:
		tapjoy_reward = client.get_tapjoy_reward()
		print(f">> Tapjoy Reward - {tapjoy_reward}")
	except Exception as e:
		print(f">> Error in get tapjoy reward - {e}")
		
def transfer_coins():
    link_Info = aminoboi.Client().get_from_link(input("Blog Link >> "))["linkInfoV2"]
    ndc_id = link_Info["extensions"]["linkInfo"]["ndcId"]; blog_Id = link_Info["extensions"]["linkInfo"]["objectId"]
    for account in accounts:
    	email = account["email"]; password = account["password"]
    	try:
    		client = aminoboi.Client()
    		auth(email=email, password=password, client=client)
    		client.join_community(ndc_id=ndc_id)
    		total_coins = client.get_wallet_info()["wallet"]["totalCoins"]
    		print(f">> {email} have {total_coins} coins...")
    		if total_coins != 0:
    			transfer = client.send_coins_blog(ndc_id=ndc_id, blog_Id=blog_Id, coins=total_coins)
    			print(f">> {email} transfered {total_coins} coins - {transfer['api:message']}...")
    	except Exception as e:
    		print(f">> Error In Transfer Coins - {e}")

def main_process():
    link_Info = aminoboi.Client().get_from_link(input("Community Link >> "))
    ndc_id = link_Info["linkInfoV2"]["extensions"]["community"]["ndcId"]
    for account in accounts:
    	client = aminoboi.Client()
    	email = account["email"]; password = account["password"]
    	try:
    		auth(email=email, password=password, client=client)
    		play_lottery(ndc_id=ndc_id, client=client); watch_ad(client=client); #get_tapjoy_reward(client=client)
    		with ThreadPoolExecutor(max_workers=100) as executor: 
    			_ = [executor.submit(generating_process(ndc_id, email, client)) for _ in range(25)]
    	except Exception as e:
    		print(f">> Error in main process - {e}")

           
		# -- transfer coins and main function for generating coins --      

def main():
	print(tabulate(menu_configs.main_menu, tablefmt="psql"))
	select = int(input("Select >> "))
	
	if select == 1:
		main_process()
	
	elif select == 2:
		transfer_coins()
	
	elif select == 3:
		autoreg_functions.auto_register(password=input("Password For All Accounts >> "))