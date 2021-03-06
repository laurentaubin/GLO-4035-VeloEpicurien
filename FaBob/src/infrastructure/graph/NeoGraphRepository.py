import logging
import random
import time
from typing import List

from py2neo import Graph, Node, NodeMatcher

from domain.graph.GraphRepository import GraphRepository


class NeoGraphRepository(GraphRepository):
    def __init__(self, host: str, port: str):
        start = time.time()
        self.__graph_client = self.__get_graph_connection(host, port)
        self.__matcher = NodeMatcher(self.__graph_client)
        print(f"\nTIME TO CONNECT TO NE04J : {time.time() - start}\n")

    def __get_graph_connection(self, host, port):
        while True:
            logging.warning("TRYING TO CONNECT TO NEO4J")
            time.sleep(1)
            try:
                return Graph(host=host, port=port)
            except Exception as e:
                logging.warning("ERROR CONNECTING TO NEO: {0}, TRYING AGAIN".format(e))
                pass

    def generate_routes(self):
        route_counter = 0
        max_route_per_resto = 10
        restaurant_counter = 0
        generated_path = []

        restaurants_nodes = []
        restaurants_table = self.__graph_client.run(
            "MATCH (r:Restaurant) RETURN r"
        ).to_table()
        for restaurant_entry in restaurants_table:
            restaurants_nodes.append(restaurant_entry[0])

        filtered_restaurants = [
            x for x in restaurants_nodes if len(x["near_segments"]) > 0
        ]

        number_of_restaurants = len(filtered_restaurants)

        for restaurant_node in filtered_restaurants:
            number_of_routes_generated = 0
            start = time.time()
            cache = []

            for _ in filtered_restaurants:
                if number_of_routes_generated >= max_route_per_resto:
                    break

                another_restaurant_node = restaurants_nodes[
                    random.randint(0, len(restaurants_nodes) - 1)
                ]

                if another_restaurant_node["restaurant_id"] in cache:
                    continue

                if (
                    restaurant_node["restaurant_id"]
                    == another_restaurant_node["restaurant_id"]
                ):
                    continue

                try:
                    query_result = self.__query_path_and_distance_between_vertex_nodes(
                        restaurant_node, another_restaurant_node
                    ).to_table()
                    distance_between_restaurants = query_result[0][0]
                    vertex_nodes_in_path_result = query_result[0][2]

                except Exception:
                    continue

                if self.__is_in_length_range(distance_between_restaurants):
                    print(
                        "DISTANCE BETWEEN RESTAURANTS: ", distance_between_restaurants
                    )

                    route_coordinates = []
                    restaurant_nodes_on_path = set()

                    for node in vertex_nodes_in_path_result:
                        if "segment_id" not in node:
                            restaurant_nodes_on_path.add(node)
                            continue

                        route_coordinates.append(
                            [
                                float(node["longitude"]),
                                float(node["latitude"]),
                            ]
                        )

                    restaurants = []
                    for restaurant_node_on_path in restaurant_nodes_on_path:
                        coordinates = [
                            float(restaurant_node_on_path["longitude"]),
                            float(restaurant_node_on_path["latitude"]),
                        ]
                        types = restaurant_node_on_path["types"]
                        restaurant_id = restaurant_node_on_path["restaurant_id"]
                        name = restaurant_node_on_path["name"]
                        restaurants.append(
                            {
                                "restaurant_id": restaurant_id,
                                "types": types,
                                "coordinates": coordinates,
                                "name": name,
                            }
                        )
                    route = {
                        "route_coordinates": route_coordinates,
                        "restaurants": restaurants,
                        "length": distance_between_restaurants,
                        "starting_point": [
                            float(restaurant_node["longitude"]),
                            float(restaurant_node["latitude"]),
                        ],
                    }
                    generated_path.append(route)
                    route_counter += 1
                    number_of_routes_generated += 1
            restaurant_counter += 1
            print(
                "ONE RESTAURANT DONE: ",
                restaurant_counter,
                "/",
                number_of_restaurants,
                " (",
                time.time() - start,
                " sec)",
            )
        return generated_path

    def get_vertex_starting_point(self, latitude: float, longitude: float):
        return {}

    def __query_path_and_distance_between_vertex_nodes(
        self, starting_node: Node, end_node: Node
    ):
        # real_query = "MATCH p=shortestPath((resto1:Restaurant)-[:on_path]->(v1:Vertex)-[r:link_to*]->(v2:Vertex)<-[:on_path]-(resto2:Restaurant)) WHERE v1.segment_id='" + str(
        #     starting_node["segment_id"]) + "' AND v1.latitude='" + str(
        #     starting_node["latitude"]) + "' AND v1.longitude='" + str(
        #     starting_node["longitude"]) + "' AND v2.segment_id='" + str(
        #     end_node["segment_id"]) + "' AND v2.latitude='" + str(end_node["latitude"]) + "' AND v2.longitude='" + str(
        #     end_node[
        #         "longitude"]) + "' WITH p, length(p) AS count ORDER BY count LIMIT 1 WITH p, relationships(p) as roads WITH p, reduce(d=0, r in roads | d + r.distance) as distance RETURN distance, round(distance) as rounded, nodes(p) as nodes"

        real_query = (
            "MATCH p=shortestPath((resto1:Restaurant)-[r:link_to*]-(resto2:Restaurant)) WHERE resto1.restaurant_id='"
            + str(starting_node["restaurant_id"])
            + "' AND resto2.restaurant_id='"
            + str(end_node["restaurant_id"])
            + "' WITH p, length(p) AS count ORDER BY count LIMIT 1 WITH p, relationships(p) as roads WITH p, reduce(d=0, r in roads | d + r.distance) as distance RETURN distance, round(distance) as rounded, nodes(p) as nodes"
        )

        return self.__graph_client.run(real_query)

    def __get_vertex_node_attributes(self, node: Node):
        return (
            "segment_id:'"
            + str(node["segment_id"])
            + "', latitude:'"
            + str(node["latitude"])
            + "', longitude:'"
            + str(node["longitude"] + "'")
        )

    def __are_equals(self, vertex_node: Node, another_vertex_node: Node):
        return (
            vertex_node["segment_id"] == another_vertex_node["segment_id"]
            and vertex_node["latitude"] == another_vertex_node["latitude"]
            and vertex_node["longitude"] == another_vertex_node["longitude"]
        )

    def __query_restaurant_nodes_on_path(self, vertex_nodes: List[Node]):
        restaurant_nodes = set()
        for vertex_node in vertex_nodes:
            query = (
                "MATCH (restaurant: Restaurant)-[:link_to]->(vertex:Vertex {"
                + self.__get_vertex_node_attributes(vertex_node)
                + "}) RETURN collect(distinct(restaurant))"
            )
            result = self.__graph_client.run(query).to_table()
            for restaurant_node in result[0][0]:
                restaurant_nodes.add(restaurant_node)
        return restaurant_nodes

    def __is_in_length_range(self, length: float):
        return (
            5000 * 0.9 <= length <= 5000 * 1.1
            or 7500 * 0.9 <= length <= 7500 * 1.1
            or 10000 * 0.9 <= length <= 10000 * 1.1
            or 12000 * 0.9 <= length <= 12000 * 1.1
            or 8000 * 0.9 <= length <= 8000 * 1.1
            or 15000 * 0.9 <= length <= 15000 * 1.1
        )
