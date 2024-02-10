from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from models import Item
from database import insert_multiple_items
from utils.user_cookies import get_user, set_user


item_list = [
  {
    "name": "Cube",
    "description": "A 6 sided shape",
    "drawing": "cube.dwg",
    "quantity": 10,
    "status": "Active"
  },
  {
      "name": "Laptop",
      "description": "15-inch laptop with an Intel Core i7 processor and 16GB RAM",
      "drawing": "/path/to/drawing/laptop.png",
      "quantity": 10,
      "status": "Active"
  },
  {
      "name": "Office Chair",
      "description": "Ergonomic office chair with adjustable height and lumbar support",
      "drawing": "/path/to/drawing/office_chair.png",
      "quantity": 5,
      "status": "Slow"
  },
  {
      "name": "Projector",
      "description": "Full HD 1080p projector with 3000 lumens brightness",
      "drawing": "/path/to/drawing/projector.png",
      "quantity": 2,
      "status": "Unavailable"
  },
  {
      "name": "Wireless Keyboard",
      "description": "Bluetooth wireless keyboard with rechargeable battery",
      "drawing": "/path/to/drawing/keyboard.pdf",
      "quantity": 15,
      "status": "Active"
  },
  {
      "name": "Coffee Machine",
      "description": "Automatic coffee machine with multiple brew settings",
      "drawing": "/path/to/drawing/coffee_machine.png",
      "quantity": 3,
      "status": "Slow"
  },
  {
      "name": "Engine",
      "description": "V8 engine with 450 horsepower",
      "drawing": "/path/to/drawing/car_parts/engine.pdf",
      "quantity": 1,
      "status": "Active"
  },
  {
      "name": "Transmission",
      "description": "6-speed automatic transmission",
      "drawing": "/path/to/drawing/car_parts/transmission.dwg",
      "quantity": 1,
      "status": "Slow"
  },
  {
      "name": "Wheel Assembly",
      "description": "18-inch alloy wheels with all-season tires",
      "drawing": "/path/to/drawing/car_parts/wheel_assembly.dwg",
      "quantity": 4,
      "status": "Active"
  },
  {
      "name": "Brake System",
      "description": "ABS brake system with electronic brakeforce distribution",
      "drawing": "/path/to/drawing/car_parts/brake_system.dwg",
      "quantity": 1,
      "status": "Unavailable"
  },
  {
      "name": "Car Seats",
      "description": "Leather-upholstered, adjustable car seats",
      "drawing": "/path/to/drawing/car_parts/car_seats.pdf",
      "quantity": 5,
      "status": "Slow"
  },
  {
      "name": "Dashboard",
      "description": "Digital dashboard with infotainment system",
      "drawing": "/path/to/drawing/car_parts/dashboard.png",
      "quantity": 1,
      "status": "Active"
  },
  {
      "name": "Exhaust System",
      "description": "Stainless steel exhaust system with catalytic converter",
      "drawing": "/path/to/drawing/car_parts/exhaust_system.dwg",
      "quantity": 1,
      "status": "Active"
  },
  {
      "name": "Headlights",
      "description": "LED headlights with automatic high beam",
      "drawing": "/path/to/drawing/car_parts/headlights.dwg",
      "quantity": 2,
      "status": "Unavailable"
  },
  {
      "name": "Battery",
      "description": "12V automotive battery",
      "drawing": "/path/to/drawing/car_parts/battery.dwg",
      "quantity": 1,
      "status": "Active"
  },
  {
      "name": "Radiator",
      "description": "Cooling radiator with integrated thermostat",
      "drawing": "/path/to/drawing/car_parts/radiator.dwg",
      "quantity": 1,
      "status": "Slow"
  },
  {
      "name": "Bolt M6x30",
      "description": "M6 size bolt, 30mm length, stainless steel",
      "drawing": "/path/to/drawing/hardware/bolt_m6x30.dwg",
      "quantity": 100,
      "status": "Active"
  },
  {
      "name": "Bolt M8x50",
      "description": "M8 size bolt, 50mm length, galvanized steel",
      "drawing": "/path/to/drawing/hardware/bolt_m8x50.dwg",
      "quantity": 75,
      "status": "Slow"
  },
  {
      "name": "Bolt M10x100",
      "description": "M10 size bolt, 100mm length, high-tensile steel",
      "drawing": "/path/to/drawing/hardware/bolt_m10x100.dwg",
      "quantity": 50,
      "status": "Unavailable"
  },
  {
      "name": "Nut M6",
      "description": "M6 size nut, stainless steel, hexagonal shape",
      "drawing": "/path/to/drawing/hardware/nut_m6.dwg",
      "quantity": 200,
      "status": "Active"
  },
  {
      "name": "Nut M8",
      "description": "M8 size nut, galvanized steel, hexagonal shape",
      "drawing": "/path/to/drawing/hardware/nut_m8.dwg",
      "quantity": 150,
      "status": "Active"
  },
  {
      "name": "Nut M10",
      "description": "M10 size nut, high-tensile steel, hexagonal shape",
      "drawing": "/path/to/drawing/hardware/nut_m10.dwg",
      "quantity": 100,
      "status": "Slow"
  },
  {
      "name": "Bolt M12x150",
      "description": "M12 size bolt, 150mm length, alloy steel",
      "drawing": "/path/to/drawing/hardware/bolt_m12x150.dwg",
      "quantity": 30,
      "status": "Slow"
  },
  {
      "name": "Nut M12",
      "description": "M12 size nut, alloy steel, hexagonal shape",
      "drawing": "/path/to/drawing/hardware/nut_m12.dwg",
      "quantity": 60,
      "status": "Unavailable"
  },
  {
      "name": "Bolt M4x20",
      "description": "M4 size bolt, 20mm length, stainless steel",
      "drawing": "/path/to/drawing/hardware/bolt_m4x20.dwg",
      "quantity": 150,
      "status": "Active"
  },
  {
      "name": "Nut M4",
      "description": "M4 size nut, stainless steel, hexagonal shape",
      "drawing": "/path/to/drawing/hardware/nut_m4.dwg",
      "quantity": 300,
      "status": "Active"
  },
  {
      "name": "Solar Panel",
      "description": "100W monocrystalline solar panel",
      "drawing": "/path/to/random/solar_panel.png",
      "quantity": 20,
      "status": "Active"
  },
  {
      "name": "Acoustic Guitar",
      "description": "Six-string acoustic guitar with spruce top",
      "drawing": "/path/to/random/acoustic_guitar.png",
      "quantity": 10,
      "status": "Slow"
  },
  {
      "name": "LED Bulb",
      "description": "10W E27 LED light bulb, warm white",
      "drawing": "/path/to/random/led_bulb.png",
      "quantity": 100,
      "status": "Active"
  },
  {
      "name": "Yoga Mat",
      "description": "Eco-friendly, non-slip yoga mat",
      "drawing": "/path/to/random/yoga_mat.png",
      "quantity": 15,
      "status": "Unavailable"
  },
  {
      "name": "Bluetooth Speaker",
      "description": "Portable Bluetooth speaker with waterproof design",
      "drawing": "/path/to/random/bluetooth_speaker.png",
      "quantity": 25,
      "status": "Active"
  },
  {
      "name": "Digital Camera",
      "description": "24MP digital SLR camera with 18-55mm lens kit",
      "drawing": "/path/to/random/digital_camera.png",
      "quantity": 5,
      "status": "Slow"
  },
  {
      "name": "Electric Drill",
      "description": "Cordless electric drill with variable speed control",
      "drawing": "/path/to/random/electric_drill.png",
      "quantity": 8,
      "status": "Active"
  },
  {
      "name": "Gardening Gloves",
      "description": "Durable leather gardening gloves, one size fits all",
      "drawing": "/path/to/random/gardening_gloves.png",
      "quantity": 30,
      "status": "Active"
  },
  {
      "name": "Telescope",
      "description": "Refractor telescope with tripod and star map",
      "drawing": "/path/to/random/telescope.png",
      "quantity": 4,
      "status": "Slow"
  },
  {
      "name": "Chess Set",
      "description": "Wooden chess set with hand-carved pieces",
      "drawing": "/path/to/random/chess_set.png",
      "quantity": 12,
      "status": "Active"
  }
]


router = APIRouter(
  prefix="/demo",
  tags=["Demo"],
  )


@router.post("/insert/")
async def create_multiple_items(user_id: str = Depends(get_user)):
    """
    Insert multiple demo items into the database.
    """
    new_items = []
    update_fields = {"update_date": datetime.now(),
                     "user_id": user_id,
                    }
    for item in item_list:
        mod_item = Item(**item)
        new_item = mod_item.model_copy(update=update_fields)
        new_items.append(new_item)
    await insert_multiple_items(new_items)
    
    response = RedirectResponse(url="/", status_code=303)
    await set_user(response, user_id)
    return response
