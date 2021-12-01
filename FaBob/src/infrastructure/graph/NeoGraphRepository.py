import logging
import time
from typing import Dict, List

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

    def generate_route(self):
        # lengths = [5000, 7500, 10000, 12000, 8000, 15000]
        lengths = [5000]

        vertex_nodes = []
        vertexes_table = self.__graph_client.run("MATCH (v:Vertex) RETURN v").to_table()
        for vertex_entry in vertexes_table:
            vertex_nodes.append(vertex_entry[0])

        for route_length in lengths:
            min_route_length = route_length * 0.9
            max_route_length = route_length * 1.1
            for vertex_node in vertex_nodes:
                for another_vertex_node in vertex_nodes:
                    if self.__are_equals(vertex_node, another_vertex_node):
                        pass
                    distance_between_vertexes = 0
                    try:
                        query_result = self.__query_distance_between_vertex_nodes(vertex_node,
                                                                                  another_vertex_node).to_table()
                        distance_between_vertexes = query_result[0][0]
                        # distance_between_vertexes = distance_between_vertexes[0][0]["distance"]
                        # print("DISTANCE FOUND: ", distance_between_vertexes, ", WITH PATH: ", path)

                        # relationships_between_vertexes = self.__query_distance_between_vertex_nodes(vertex_node,
                        #                                                                             another_vertex_node).to_table()
                        # print(relationships_between_vertexes)
                        # print("length of relationships: ", len(relationships_between_vertexes))
                        # # print("DISTANCE CALCULATED OF PATH: ", str(distance_between_vertexes))
                        # if len(relationships_between_vertexes) == 0:
                        #     print("NO PATH FOUND\n")
                        #     pass
                    except Exception as err:
                        print("ERROR while querying distance: ", err, "meaning vertexes cannot be connected")
                        pass
                    if min_route_length <= distance_between_vertexes <= max_route_length:
                        print("\nPATH FOUND WITH DISTANCE: ", str(distance_between_vertexes), "\n")
                        nodes_in_route = self.__query_vertexes_forming_valid_route(vertex_node,
                                                                                   another_vertex_node).to_table()
                        print("VERTEXES IN FOUND PATH: \n", nodes_in_route)

                        # print("NODES FOR FOUND ROUTE:")
                        # for node_entry in nodes_in_route:
                        #     print(node_entry[0])

    def get_vertex_starting_point(self, latitude: float, longitude: float):
        return {}

    def __query_distance_between_vertex_nodes(self, starting_node: Node, end_node: Node):
        real_query = "MATCH p=shortestPath((v1:Vertex)-[r:link_to*]->(v2:Vertex)) WHERE v1.segment_id='" + str(
            starting_node["segment_id"]) + "' AND v1.latitude='" + str(
            starting_node["latitude"]) + "' AND v1.longitude='" + str(
            starting_node["longitude"]) + "' AND v2.segment_id='" + str(
            end_node["segment_id"]) + "' AND v2.latitude='" + str(end_node["latitude"]) + "' AND v2.longitude='" + str(
            end_node[
                "longitude"]) + "' WITH p, length(p) AS count ORDER BY count LIMIT 1 WITH relationships(p) as roads WITH reduce(d=0, r in roads | d + r.distance) as distance RETURN distance, round(distance) as rounded"

        return self.__graph_client.run(
            real_query)

    def __query_vertexes_forming_valid_route(self, starting_node: Node, end_node: Node):
        query = "MATCH p=shortestPath((v1:Vertex)-[r:link_to*]->(v2:Vertex)) WHERE v1.segment_id='" + str(
            starting_node["segment_id"]) + "' AND v1.latitude='" + str(
            starting_node["latitude"]) + "' AND v1.longitude='" + str(
            starting_node["longitude"]) + "' AND v2.segment_id='" + str(
            end_node["segment_id"]) + "' AND v2.latitude='" + str(end_node["latitude"]) + "' AND v2.longitude='" + str(
            end_node[
                "longitude"]) + "' WITH p, length(p) AS count ORDER BY count LIMIT 1 RETURN nodes(p)"
        return self.__graph_client.run(query)

    def __get_vertex_node_attributes(self, node: Node):
        return "segment_id:'" + str(node['segment_id']) + "', latitude:'" + str(
            node["latitude"]) + "', longitude:'" + str(
            node["longitude"] + "'")

    def __are_equals(self, vertex_node: Node, another_vertex_node: Node):
        return vertex_node["segment_id"] == another_vertex_node["segment_id"] and vertex_node["latitude"] == \
               another_vertex_node["latitude"] and vertex_node["longitude"] == another_vertex_node["longitude"]
