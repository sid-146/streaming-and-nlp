from pymongo.collection import Collection


def query_checkpoint(client: Collection, process_name: str):
    # Client will be given till the collection
    response = client.find_one(filter={"process_name": process_name})
    return response
