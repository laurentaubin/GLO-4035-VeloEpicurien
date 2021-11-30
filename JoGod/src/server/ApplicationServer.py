from flask import Flask
import markdown
import markdown.extensions.fenced_code
import markdown.extensions.tables

from api.ExtractedDataResource import ExtractedDataResource
from api.HeartbeatResource import HeartbeatResource
from api.ReadMeResource import ReadMeResource
from api.TransformedDataResource import TransformedDataResource


class ApplicationServer:
    def __init__(
            self,
            heartbeat_resource: HeartbeatResource,
            readme_resource: ReadMeResource,
            extracted_data_resource: ExtractedDataResource,
            transformed_data_resource: TransformedDataResource,
    ):
        self.__heartbeat_resource = heartbeat_resource
        self.__readme_resource = readme_resource
        self.__extracted_data_resource = extracted_data_resource
        self.__transformed_data_resource = transformed_data_resource

        self.__app = Flask(__name__)
        self.__app.config["JSON_AS_ASCII"] = False
        self.__app.add_url_rule("/heartbeat", "heartbeat", self.__send_heartbeat)

        self.__app.add_url_rule("/readme", "readme", self.__get_readme)

        self.__app.add_url_rule(
            "/extracted_data", "extracted_data", self.__get_extracted_data
        )
        self.__app.add_url_rule(
            "/transformed_data", "transformed_data", self.__get_transformed_data
        )

    def run(self, hostname) -> None:
        self.__app.run(hostname)

    def __send_heartbeat(self) -> dict:
        return self.__heartbeat_resource.send_heartbeat().to_dict()

    def __get_readme(self) -> str:
        readme_text = self.__readme_resource.get_readme()
        return markdown.markdown(readme_text, extensions=["fenced_code", "tables"])

    def __get_extracted_data(self) -> dict:
        return self.__extracted_data_resource.get_extracted_data()

    def __get_transformed_data(self) -> dict:
        return self.__transformed_data_resource.get_transformed_data()
