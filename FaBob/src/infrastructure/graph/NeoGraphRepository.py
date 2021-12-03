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

    def generate_routes_resto_to_resto(self):
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

        number_of_restaurants = len(restaurants_nodes)

        for restaurant_node in restaurants_nodes:
            number_of_routes_generated = 0
            start = time.time()
            for another_restaurant_node in restaurants_nodes:
                if number_of_routes_generated >= max_route_per_resto:
                    break

                if restaurant_node["restaurant_id"] == another_restaurant_node["restaurant_id"]:
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

                    for vertex_node_in_path in vertex_nodes_in_path_result:
                        if "segment_id" not in vertex_node_in_path:
                            continue

                        route_coordinates.append(
                            [
                                float(vertex_node_in_path["longitude"]),
                                float(vertex_node_in_path["latitude"]),
                            ]
                        )

                    restaurant_nodes = self.__query_restaurant_nodes_on_path(
                        vertex_nodes_in_path_result
                    )
                    restaurants = []
                    for restaurant_node in restaurant_nodes:
                        coordinates = [
                            float(restaurant_node["longitude"]),
                            float(restaurant_node["latitude"]),
                        ]
                        types = restaurant_node["types"]
                        restaurant_id = restaurant_node["restaurant_id"]
                        name = restaurant_node["name"]
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
                "ONE RESTAURANT DONE: ", restaurant_counter, "/", number_of_restaurants, " (", time.time() - start,
                " sec)"
            )
        return generated_path

    def generate_routes(self):
        generated_path = []
        max_number_of_path_per_vertex = 5
        path_counter = 0

        vertex_nodes = []
        vertexes_table = self.__graph_client.run("MATCH (v:Vertex) RETURN v").to_table()
        for vertex_entry in vertexes_table:
            vertex_nodes.append(vertex_entry[0])

        number_of_vertexes = len(vertex_nodes)

        for index in range(number_of_vertexes):
            vertex_node = vertex_nodes[index]
            index += 1000
            already_generated_path = set()
            while path_counter < max_number_of_path_per_vertex:
                if path_counter >= max_number_of_path_per_vertex:
                    break
                another_vertex_node_index = random.randint(0, number_of_vertexes)
                another_vertex_node = vertex_nodes[another_vertex_node_index]

                if another_vertex_node in already_generated_path or self.__are_equals(
                        vertex_node, another_vertex_node
                ):
                    continue

                already_generated_path.add(another_vertex_node)

                distance_between_vertexes = 0
                vertex_nodes_in_path_result = None

                try:
                    query_result = self.__query_path_and_distance_between_vertex_nodes(
                        vertex_node, another_vertex_node
                    ).to_table()
                    distance_between_vertexes = query_result[0][0]
                    vertex_nodes_in_path_result = query_result[0][2]
                except Exception:
                    continue

                if self.__is_in_length_range(distance_between_vertexes):
                    path_counter += 1
                    route_coordinates = []

                    for vertex_node_in_path in vertex_nodes_in_path_result:
                        print("RESTO ID: ", vertex_node_in_path["restaurant_id"])

                        try:
                            vertex_node_in_path["segment_id"]
                        except Exception:
                            print("is a resto")
                            continue

                        route_coordinates.append(
                            [
                                float(vertex_node_in_path["longitude"]),
                                float(vertex_node_in_path["latitude"]),
                            ]
                        )

                    restaurant_nodes = self.__query_restaurant_nodes_on_path(
                        vertex_nodes_in_path_result
                    )
                    restaurants = []
                    for restaurant_node in restaurant_nodes:
                        coordinates = [
                            restaurant_node["longitude"],
                            restaurant_node["latitude"],
                        ]
                        types = restaurant_node["types"]
                        restaurant_id = restaurant_node["restaurant_id"]
                        restaurants.append(
                            {
                                "restaurant_id": restaurant_id,
                                "types": types,
                                "coordinates": coordinates,
                            }
                        )

                    generated_path.append(
                        {
                            "route_coordinates": route_coordinates,
                            "restaurants": restaurants,
                        }
                    )
                    print(
                        "PATH ADDED: ",
                        path_counter,
                        "/",
                        max_number_of_path_per_vertex,
                        ", DISTANCE: ",
                        distance_between_vertexes,
                    )
            print("\nONE VERTEX DONE, RESET PATH COUNTER FOR NEW VERTEX")
            path_counter = 0
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
