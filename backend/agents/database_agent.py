from uagents import Agent, Context, Model
from uagents.query import query
from uagents.setup import fund_agent_if_low
import requests
import json
import csv
import math

json_file_path = r'C:\Users\a21ma\OneDrive\Desktop\Code\Projects\Cyber Cypher 3.0\backend\restocking_prediction\predictions.json'
csv_file_path = r'C:\Users\a21ma\OneDrive\Desktop\Code\Projects\Cyber Cypher 3.0\data\products.csv'

# Reading the data from the json file:
# with open(json_file_path, 'r') as json_file:
#     database_response = json.load(json_file)
# print(database_response[0])
    
response = requests.get('http://localhost:5000/products')
database_response = response.json()

with open(json_file_path, 'r') as json_file:
    stock_predictions = json.load(json_file)
# print(stock_predictions)


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
    
    input_names_with_size = msg.product.split(', ')
    input_names = [name.split(' -')[0] for name in input_names_with_size]
    input_sizes = [name.split('- ')[1] for name in input_names_with_size]
    input_quantities = msg.quantity.split(', ')
    # print(input_names,input_sizes,input_quantities)
    
    for data in database_response:
        # print(data)
        
        data_name_lower=data['Name'].lower()
        data_quantity = int(data['Quantity'])
        data_id = data['id']
        data_size = data['Size']
        
        
        for i in range(len(input_names)):
            
            input_name_lower=input_names[i].lower()
            input_quantity = int(input_quantities[i])
            input_size = input_sizes[i]
            
            if data_name_lower == input_name_lower and data_size == input_size:
                print(f'{input_quantity} of {input_names[i]}(id:{data_id}) was bought')
                
                product_stock = stock_predictions[data_id-1]
                min_stock = math.ceil(0.25 * product_stock['Month_1']) # month 1 because it is currently january so we are using predictions for this month
                
                
                # if data_quantity < min_stock:
                #     # print('Low stock before buying')
                #     await ctx.send("agent1qfhsacmleeygp9qhpnsyjnsmj36el3far8k6vpep5t8uuxupnhus7t40wv8", Message(product=input_names_with_size[i],quantity=data['Quantity'])) #goes to alert agent
                    
                newQuantity = data_quantity - input_quantity
                data['Quantity'] = newQuantity
                
                restock_quantity = math.ceil(product_stock['Month_1'] - newQuantity)
                
                response=requests.post('http://localhost:5000/products', json=database_response)
                # Updating the json file:
                # with open(json_file_path, 'w') as json_file:
                #     json.dump(database_response, json_file, indent=2)
                
                    
                # Reading the csv file:
                with open(csv_file_path, 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    csv_data = list(csv_reader)
                    
                # Updating csv values
                for csv_data_row in csv_data:
                    if int(csv_data_row['id']) == data_id:
                        csv_data_row['Quantity'] = newQuantity
                
                with open(csv_file_path, 'w', newline='') as csv_file:
                    fieldnames = ["id", "Name", "Brand", "Category", "SubCategory", "Price", "Size", "Quantity"]
                    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                    # Write the header
                    csv_writer.writeheader()

                    # Write the updated data
                    csv_writer.writerows(csv_data)
                
                print("New Quantity: ",data['Quantity']) 
                if data['Quantity'] < min_stock:
                    # print('Low stock after buying')
                    await ctx.send("agent1qfhsacmleeygp9qhpnsyjnsmj36el3far8k6vpep5t8uuxupnhus7t40wv8", Message(product=input_names_with_size[i],quantity=restock_quantity)) # goes to alert agent




if __name__ == "__main__":
    fund_agent_if_low(database_agent.wallet.address())
    database_agent.run()

