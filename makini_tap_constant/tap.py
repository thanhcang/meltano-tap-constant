import json
import os
from singer_sdk import Tap, Stream
from singer_sdk import typing as th
from singer_sdk.helpers._util import utc_now

class ConstantStream(Stream):
    """Stream class for constant data."""
    name = "constant_stream"
    schema = th.PropertiesList(
        th.Property("name", th.StringType, required=False, description="Name of the entity"),
        th.Property("data", th.ArrayType(
            th.ObjectType(
                th.Property("code", th.StringType),
                th.Property("name", th.StringType)
            )
        ), required=False, description="List of data"),
    ).to_dict()

    def __init__(self, tap, constant_data):
        super().__init__(tap)
        self.constant_data = constant_data
        self.logger = tap.logger 

    def get_records(self, context=None):
        """Yields records for the stream."""
        for stream in self.constant_data:
            collection_name = stream["name"]  # Use the 'name' field as the collection name
            for status in stream["data"]:
                # Create a record for each entry in the 'data' array
                record = {
                    "name": status,
                    "code": status
                }
                self.logger.info(f"Yielding record for {collection_name}: {record}")
                yield record

class TapConstant(Tap):
    """A tap to handle constant data."""
    name = "meltano-tap-constant"

    # Define the constant data
    constant_data = [
        {
            "name": "work_orders_statuses",
            "data": ["new", "open", "onhold"]
        },
        {
            "name": "work_orders_statuses-2",
            "data": ["new", "open", "onhold"]
        },
    ]

    def discover_streams(self):
        """Returns a list of streams that the tap can sync."""
        return [
            ConstantStream(self, self.constant_data)
        ]
    
if __name__ == "__main__":
    TapConstant.cli()    