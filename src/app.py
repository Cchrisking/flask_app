#!/usr/bin/env python3
from flask import Flask, request
app = Flask(__name__)
@app.route("/")
def main():
    return '''
     <form action="/echo_user_input" method="POST">
    <label for="rig_price">Rig Price ($):</label>
    <input type="number" step="0.01" name="rig_price" id="rig_price"><br><br>

    <label for="hash_power">Hash Power (TH/s per rig):</label>
    <input type="number" step="0.01" name="hash_power" id="hash_power"><br><br>

    <label for="rig_number">Number of Rigs:</label>
    <input type="number" name="rig_number" id="rig_number"><br><br>

    <label for="power_consumption">Power Consumption (watts per rig):</label>
    <input type="number" step="0.01" name="power_consumption" id="power_consumption"><br><br>

    <label for="cost_kwh">Electricity Cost ($/kWh):</label>
    <input type="number" step="0.0001" name="cost_kwh" id="cost_kwh"><br><br>

    <label for="pool_fee">Pool Fee (%):</label>
    <input type="number" step="0.01" name="pool_fee" id="pool_fee"><br><br>

    <input type="submit" value="Submit!">
</form>
     '''
@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    # Convert inputs to floats (with sane defaults to avoid crashes)
    input_rig_cost = float(request.form.get("rig_price", 0))
    input_hash = float(request.form.get("hash_power", 0))       # TH/s per rig
    input_rig = float(request.form.get("rig_number", 0))        # number of rigs
    input_consumption = float(request.form.get("power_consumption", 0))  # watts per rig
    input_cost = float(request.form.get("cost_kwh", 0))         # $/kWh
    input_fee = float(request.form.get("pool_fee", 0))          # % (e.g. 1 = 1%)

    if input_rig == 0 or input_hash == 0:
        return "Please provide valid rig number and hash power."

    # Totals across all rigs
    t_rig_cost = input_rig * input_rig_cost          # total investment ($)
    t_hash_power = input_hash * input_rig             # total hash power (TH/s)
    t_consumption_kw = (input_consumption * input_rig) / 1000  # total power in kW
    t_daily_power_cost = t_consumption_kw * 24 * input_cost    # daily electricity cost ($)

    # Mining assumptions
    btc_price = 65000
    daily_btc_per_th = 0.0001927  # BTC mined per day, per TH/s (adjust to current network difficulty)

    daily_btc_mined = t_hash_power * daily_btc_per_th
    daily_revenue = daily_btc_mined * btc_price
    daily_revenue_after_fee = daily_revenue * (1 - input_fee / 100)

    daily_profit = daily_revenue_after_fee - t_daily_power_cost

    if daily_profit <= 0:
        return "This setup is not profitable at current settings — ROI is infinite (never breaks even)."

    rig_roi = t_rig_cost / (daily_profit * 365)  # years to break even

    return f"ROI: {rig_roi:.2f} years"
