from uagents import Agent, Context, Model
from uagents.query import query
from uagents.setup import fund_agent_if_low
import requests
import json

json_file_path = r'C:\Users\a21ma\OneDrive\Desktop\Cyber Cypher 3.0\data\products.json'

with open(json_file_path, 'r') as json_file:
    database_response = json.load(json_file)
# print(database_response[0])
    
class Message(Model):
    product: str
    quantity: str

database_agent = Agent(
    name="database_agent",
    seed="database_agent_seed",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# print(database_agent.address)

@database_agent.on_message(model=Message)
async def handle_message(ctx:Context,sender:str, msg: Message):
    
    input_names = msg.product.split(',')
    input_quantities = msg.quantity.split(',')
    
    for data in database_response:
        # print(data)
        
        data_name_lower=data['Name'].lower()
        Quantity = int(data['Quantity'])
        data_id = data['id']
        
        
        for i in range(len(input_names)):
            
            input_name_lower=input_names[i].lower()
            input_quantity = int(input_quantities[i])
            
            if data_name_lower == input_name_lower:
                print(f'{input_quantity} of {input_names[i]}(id:{data_id}) was bought')
                if Quantity <35:
                    # print('Low stock before buying')
                    await ctx.send("agent1qfhsacmleeygp9qhpnsyjnsmj36el3far8k6vpep5t8uuxupnhus7t40wv8", Message(value=data_name_lower))
                newQuantity = Quantity - input_quantity
                data = {
                "Quantity": newQuantity
                }  

                headers = {
                    "Content-Type": "application/json"
                }
                
                # response = requests.put(database_api_url+'/{data_id}', json=data, headers=headers)
                # print(response.status_code)
                
                
                
                print("New Quantity: ",data['Quantity']) 
                if data['Quantity'] <5:
                    # print('Low stock after buying')
                    await ctx.send("agent1qfhsacmleeygp9qhpnsyjnsmj36el3far8k6vpep5t8uuxupnhus7t40wv8", Message(value=data_name_lower))
                    
                    
            

if __name__ == "__main__":
    fund_agent_if_low(database_agent.wallet.address())
    database_agent.run()

