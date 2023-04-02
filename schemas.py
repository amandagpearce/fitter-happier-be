from marshmallow import Schema, fields

# schemas used for validating incoming data and returning valid data


class ItemSchema(Schema):
    id = fields.Str(
        dump_only=True
    )  # won't be used for validation, only used for returning data
    name = fields.Str(required=True)  # must be in the payload json
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()  # not name or price are required but can be received
    price = fields.Float()


class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
