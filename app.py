from edifice import Lineage
import json

# Example lineage data
table1_name = "Customers"
table2_name = "Orders"
lineage_data = Lineage(
    source_table=table1_name,
    target_table=table2_name,
    columns=[
        ("customer_id", "customer_id"),
        ("order_id", "order_id"),
    ],
)
with open("datatracer/datasets/posts/metadata.json","r") as read_file:
    data = json.loads(read_file.read())

related_entities = data

# Define app layout
app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="lineage-graph"),
    dcc.Dropdown(
        id="related-entities",
        options=[{"label": entity, "value": entity} for entity in related_entities.keys()],
        placeholder="Show related entities",
    ),
    dcc.Button("Refresh", id="refresh-button"),
])

@app.callback(
    Output("lineage-graph", "figure"),
    [Input("source-table", "value"), Input("target-table", "value")],
    State("related-entities", "value"),
)
def update_graph(source_table, target_table, related_entities):
    # Use Pyedifice to generate lineage graph
    graph = lineage_data.to_pyedifice_graph(related_entities=related_entities)
    return graph.render_plotly()

if __name__ == "__main__":
    app.run_server(debug=True)