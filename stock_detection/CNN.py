from roboflow import Roboflow
rf = Roboflow(api_key="") # You can get your free key at https://universe.roboflow.com/samrat-sahoo/groceries-6pfog/model/6 in the Hosted API section 
project = rf.workspace().project("groceries-6pfog")
model = project.version(6).model

model.predict("stock_detection/test2.png", confidence=50, overlap=30).save("prediction2.jpg")
