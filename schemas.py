from marshmallow import Schema, fields

# schemas used for validating incoming data and returning valid data
# plain schemas fix recursive nesting in schemas with relationships


class PlainExerciseSchema(
    Schema
):  # an item schema that doesnt deal with stores at all
    id = fields.Int(
        dump_only=True
    )  # won't be used for validation, only used for returning data
    name = fields.Str(required=False)  # must be in the payload json
    type = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class PlainVideoSchema(Schema):
    id = fields.Int(dump_only=True)
    yt_id = fields.Str(required=True)
    title = fields.Str(required=True)


class ExerciseUpdateSchema(Schema):
    name = fields.Str(required=False)
    type = fields.Str(required=False)


class ExerciseSchema(PlainExerciseSchema):
    user_id = fields.Int(required=True, load_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))
    videos = fields.List(fields.Nested(PlainVideoSchema(), dump_only=True))


class VideoSchema(PlainVideoSchema):
    exercises = fields.List(fields.Nested(PlainExerciseSchema()))


class TagSchema(PlainTagSchema):
    user_id = fields.Int(load_only=True)
    exercises = fields.List(
        fields.Nested(PlainExerciseSchema()), dump_only=True
    )


class TagAndExerciseSchema(Schema):
    exercise = fields.Nested(ExerciseSchema)
    tag = fields.Nested(TagSchema)


class VideoAndExerciseSchema(Schema):
    exercise = fields.Nested(ExerciseSchema)
    video = fields.Nested(VideoSchema)


class ExerciseLogSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    exercises = fields.List(
        fields.Nested(PlainExerciseSchema()), dump_only=True
    )


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(
        required=True, load_only=True
    )  # load_only=True ensures the pw will never be returned to the client


class TokenBlocklist(Schema):
    token = fields.Str(required=True, load_only=True)


# load_only -> receiving data from client
# dump_only -> sending data to client
