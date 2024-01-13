from uagents import Agent, Context, Model
from uagents.query import query
from uagents.setup import fund_agent_if_low
import requests
import csv
import json

# database_api_url = "https://northwind.vercel.app/api/products"

# database_response = requests.get(database_api_url)

def api_csv_to_json(api_url):
    # Make a GET request to the API
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Decode the response content as UTF-8 and create a CSV reader
        csv_data = response.content.decode('utf-8').splitlines()
        csv_reader = csv.DictReader(csv_data)

        # Convert CSV to a list of dictionaries
        data = list(csv_reader)

        # Convert list of dictionaries to JSON format
        json_data = json.dumps(data, indent=2)

        return json_data
    else:
        print(f'Failed to fetch data from API. Status code: {response.status_code}')
        return None

# Specify the API URL
api_url = 'https://raw.githubusercontent.com/abhaymathur21/Cyber-Cypher-3.0/main/data/products.csv'

# Convert API CSV data to JSON
database_response = json.loads(api_csv_to_json(api_url))

# input_names=['tofu','outback lager']

class Message(Model):
    value: str

database_agent = Agent(
    name="database_agent",
    seed="database_agent_seed",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

print(database_agent.address)

@database_agent.on_message(model=Message)
async def handle_message(ctx:Context,sender:str, msg: Message):
    
    input_names = msg.value.split(',')
    
    for data in database_response:
        # print(data)
        data_name_lower=data['Name'].lower()
        Quantity = data['Quantity']
        # data_id = data['id']
        
        
        for input_name in input_names:
            
            input_name_lower=input_name.lower()
            
            if data_name_lower == input_name_lower:
                print('True')
                if Quantity <5:
                    # print('Low stock before buying')
                    await ctx.send("agent1qfhsacmleeygp9qhpnsyjnsmj36el3far8k6vpep5t8uuxupnhus7t40wv8", Message(value=data_name_lower))
                newQuantity = Quantity - 11
                data = {
                "Quantity": newQuantity
                }  

                headers = {
                    "Content-Type": "application/json"
                }
                
                # response = requests.put(database_api_url+'/{data_id}', json=data, headers=headers)
                # print(response.status_code)
                print(data['Quantity']) 
                if data['Quantity'] <5:
                    # print('Low stock after buying')
                    await ctx.send("agent1qfhsacmleeygp9qhpnsyjnsmj36el3far8k6vpep5t8uuxupnhus7t40wv8", Message(value=data_name_lower))
                    
                    
            

if __name__ == "__main__":
    fund_agent_if_low(database_agent.wallet.address())
    database_agent.run()

