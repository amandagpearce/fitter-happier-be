from marshmallow import Schema, fields

# schemas used for validating incoming data and returning valid data
# plain schemas fix recursive nesting in schemas with relationships


class PlainItemSchema(
    Schema
):  # an item schema that doesnt deal with stores at all
    id = fields.Str(
        dump_only=True
    )  # won't be used for validation, only used for returning data
    name = fields.Str(required=True)  # must be in the payload json
    price = fields.Float(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()  # not name or price are required but can be received
    price = fields.Float()


class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemSchema(PlainItemSchema):
    store_id = (
        fields.Int(required=True, load_only=True),
    )  # whenever we receive data from client we'll pass the store_id
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


# load_only -> receiving data from client
# dump_only -> sending data to client
