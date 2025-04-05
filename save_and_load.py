import json
import xml.etree.ElementTree as ET
import os
from pymongo import MongoClient
import datetime

class MongoSaveManager:
    def __init__(self, db_name="tower_defense", collection_name="save_data"):
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save(self, data):
        data["timestamp"] = datetime.datetime.utcnow()
        self.collection.delete_many({})  # Zostaw tylko jedno save
        self.collection.insert_one(data)

    def load(self):
        latest = self.collection.find_one(sort=[("timestamp", -1)])
        return latest if latest else None
class JSONSaveManager:
    def __init__(self, file_path="data.json"):
        self.file_path = file_path

    def save(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return None
class XMLSaveManager:
    def __init__(self, file_path="data.xml"):
        self.file_path = file_path

    def save(self, data):
        root = ET.Element("save")

        ET.SubElement(root, "level").text = str(data.get("level", 1))
        ET.SubElement(root, "hp").text = str(data.get("hp", 10))
        ET.SubElement(root, "money").text = str(data.get("money", 1000))
        ET.SubElement(root, "wave").text = str(data.get("wave", 0))

        turrets_el = ET.SubElement(root, "turrets")
        for turret in data.get("turrets", []):
            t_el = ET.SubElement(turrets_el, "turret")
            t_el.set("x", str(turret["x"]))
            t_el.set("y", str(turret["y"]))
            t_el.set("type", turret["type"])
            t_el.set("level", str(turret["level"]))

        enemies_el = ET.SubElement(root, "enemy_data")
        for key, val in data.get("enemy_data", {}).items():
            enemy = ET.SubElement(enemies_el, "enemy")
            enemy.set("type", key)
            enemy.set("count", str(val))

        config = data.get("config", {})
        config_el = ET.SubElement(root, "config")
        ET.SubElement(config_el, "mode").text = config.get("mode", "single")
        ET.SubElement(config_el, "ip").text = str(config.get("ip", ""))
        ET.SubElement(config_el, "port").text = str(config.get("port", ""))

        tree = ET.ElementTree(root)
        tree.write(self.file_path, encoding="utf-8", xml_declaration=True)

    def load(self):
        if not os.path.exists(self.file_path):
            return None

        tree = ET.parse(self.file_path)
        root = tree.getroot()

        data = {
            "level": int(root.findtext("level")),
            "hp": int(root.findtext("hp")),
            "money": int(root.findtext("money")),
            "wave": int(root.findtext("wave")),
            "turrets": [],
            "enemy_data": {},
            "config": {}
        }

        for t in root.find("turrets"):
            data["turrets"].append({
                "x": int(t.get("x")),
                "y": int(t.get("y")),
                "type": t.get("type"),
                "level": int(t.get("level"))
            })

        for e in root.find("enemy_data"):
            data["enemy_data"][e.get("type")] = int(e.get("count"))

        config = root.find("config")
        data["config"] = {
            "mode": config.findtext("mode"),
            "ip": config.findtext("ip"),
            "port": int(config.findtext("port") or 0)
        }

        return data
xml_manager=XMLSaveManager()
json_manager=JSONSaveManager()
mongodb_manager=MongoSaveManager()