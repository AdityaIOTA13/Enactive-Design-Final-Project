import json
import rhinoscriptsyntax as rs
import os

def extract_geometry_from_response(json_path):
    """
    Extract geometry data from the response JSON file.
    """
    if not os.path.exists(json_path):
        raise Exception("JSON file not found: " + json_path)

    with open(json_path, "r") as file:
        response = json.load(file)

    # Extract the content field
    content = response.get("choices", [])[0].get("message", {}).get("content", "")

    # Find and parse the JSON block in the content
    start_index = content.find("{")
    end_index = content.rfind("}")
    if start_index == -1 or end_index == -1:
        raise Exception("No JSON block found in the response content.")

    geometry_json = content[start_index:end_index+1]
    return json.loads(geometry_json)

def create_rhino_model_from_json(geometry_data):
    """
    Parse extracted geometry data and create corresponding Rhino geometry.
    """
    drawing = geometry_data.get("Drawing", {})

    # Add Nodes
    nodes = {}
    for node in drawing.get("Nodes", []):
        node_id = node["nodeID"]
        coordinates = node["coordinates"]
        nodes[node_id] = (coordinates["x"], coordinates["y"], coordinates["z"])

    # Add Edges
    for edge in drawing.get("Edges", []):
        start_node = nodes[edge["nodeStart"]]
        end_node = nodes[edge["nodeEnd"]]
        rs.AddLine(start_node, end_node)

    # Add Circles
    for circle in drawing.get("Circles", []):
        center_node = nodes[circle["centerNode"]]
        radius = circle["radius"]
        rs.AddCircle(center_node, radius)

    # Add Arcs
    for arc in drawing.get("Arcs", []):
        center_node = nodes[arc["centerNode"]]
        radius = arc["radius"]
        start_angle = arc["startAngle"]
        end_angle = arc["endAngle"]
        rs.AddArc(center_node, radius, start_angle, end_angle)

    print("Rhino model created successfully!")

if __name__ == "__main__":
    # Path to JSON file
    json_path = "/Users/adityaagarwal/Downloads/image2rhino/output/drawing_output.json"
    print("Using JSON file at: " + json_path)

    try:
        # Extract and parse geometry data
        geometry_data = extract_geometry_from_response(json_path)

        # Create geometry in Rhino
        create_rhino_model_from_json(geometry_data)
    except Exception as e:
        print("Error: " + str(e))
