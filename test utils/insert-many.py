import requests


item_insert = [
  {
    "name": "Cube",
    "description": "6 Sides",
    "drawing": "cube.dwg",
    "quantity": 10,
    "status": "Active"
  },
  {
   "name": "Bolt 0.50",
   "description": "0.50in Bolt",
   "drawing": "bolt_50.dwg",
   "quantity": 100,
   "status": "Active"
  },
  {
   "name": "Bolt 0.25",
   "description": "0.250in Bolt",
   "drawing": "bolt_25.dwg",
   "quantity": 230,
   "status": "Active"
  },
  {
   "name": "Bolt 0.125",
   "description": "0.1250in Bolt",
   "drawing": "bolt_125.dwg",
   "quantity": 12,
   "status": "Active"
  },
  {
   "name": "Bolt 1",
   "description": "1.0in Bolt",
   "drawing": "bolt_1000.dwg",
   "quantity": 2,
   "status": "Unavailable"
  },
]

response = requests.post("http://localhost:8000/api/insert/", json=item_insert)
print(response.text)