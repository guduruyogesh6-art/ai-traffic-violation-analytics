class TrafficAI:
    def __init__(self):
        self.rules = {
            "speed_limit": 60
        }

    def predict(self, vehicle_speed):
        if vehicle_speed > self.rules["speed_limit"]:
            return "🚨 Overspeed Violation Detected"
        else:
            return "✅ No Violation"
