from uagents import Agent, Context, Model
from uagents.query import query
from uagents.setup import fund_agent_if_low
import requests
import json
import csv

json_file_path = r'C:\Users\a21ma\OneDrive\Desktop\Cyber Cypher 3.0\data\products.json'
csv_file_path = r'C:\Users\a21ma\OneDrive\Desktop\Cyber Cypher 3.0\data\products.csv'

# Reading the data from the json file:
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
                    await ctx.send("agent1qfhsacmleeygp9qhpnsyjnsmj36el3far8k6vpep5t8uuxupnhus7t40wv8", Message(value=data_name_lower)) #goes to alert agent
                    
                newQuantity = Quantity - input_quantity
                data['Quantity'] = newQuantity
                
                # Updating the json file:
                with open(json_file_path, 'w') as json_file:
                    json.dump(database_response, json_file, indent=2)
                    
                # Reading the csv file:
                with open(csv_file_path, 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    csv_data = list(csv_reader)
                    
                # Updating csv values
                for csv_data_row in csv_data:
                    if int(csv_data_row['id']) == data_id:
                        csv_data_row['Quantity'] = newQuantity
                
                with open(csv_file_path, 'w', newline='') as csv_file:
                    fieldnames = ["id", "Name", "Brand", "Category", "SubCategory", "Price", "Quantity"]
                    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                    # Write the header
                    csv_writer.writeheader()

                    # Write the updated data
                    csv_writer.writerows(csv_data)
                
                print("New Quantity: ",data['Quantity']) 
                if data['Quantity'] <5:
                    # print('Low stock after buying')
                    await ctx.send("agent1qfhsacmleeygp9qhpnsyjnsmj36el3far8k6vpep5t8uuxupnhus7t40wv8", Message(value=data_name_lower)) # goes to alert agent




if __name__ == "__main__":
    fund_agent_if_low(database_agent.wallet.address())
    database_agent.run()

