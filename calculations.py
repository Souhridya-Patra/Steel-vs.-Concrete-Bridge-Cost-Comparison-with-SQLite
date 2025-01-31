import sqlite3

def database():
    db_name = "bridge_costs.db"
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM rates")
    all_rows = cursor.fetchall()
    connection.close()
    return all_rows

def calculate_costs(span_length, width, traffic_volume, design_life):
    db_values = database()[0]

    steel_costs = {
        "Construction Cost": span_length * width * db_values[1],
        "Maintenance Cost": span_length * width * db_values[2] * design_life,
        "Repair Cost": span_length * width * db_values[3],
        "Demolition Cost": span_length * width * db_values[4],
        "Environmental Cost": span_length * width * db_values[5],
        "Social Cost": traffic_volume * design_life * db_values[6],
        "User Cost": traffic_volume * design_life * db_values[7],
    }
    steel_costs["Total Cost"] = sum(steel_costs.values())

    concrete_costs = {
        "Construction Cost": span_length * width * db_values[8],
        "Maintenance Cost": span_length * width * db_values[9] * design_life,
        "Repair Cost": span_length * width * db_values[10],
        "Demolition Cost": span_length * width * db_values[11],
        "Environmental Cost": span_length * width * db_values[12],
        "Social Cost": traffic_volume * design_life * db_values[13],
        "User Cost": traffic_volume * design_life * db_values[14],
    }
    concrete_costs["Total Cost"] = sum(concrete_costs.values())

    return steel_costs, concrete_costs
