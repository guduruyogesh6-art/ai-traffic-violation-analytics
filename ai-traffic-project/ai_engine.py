class TrafficAI:

    def predict_traffic(self, vehicles, violations):

        score = vehicles + (violations * 2)

        if score < 20:
            return "Low Traffic"
        elif score < 50:
            return "Medium Traffic"
        else:
            return "Heavy Traffic"

    def risk_level(self, violations):

        if violations > 10:
            return "High Risk Zone"
        elif violations > 5:
            return "Medium Risk Zone"
        else:
            return "Low Risk Zone"
