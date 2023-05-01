from marshmallow import Schema, fields

# schemas utilizados para validar dados recebidos e retornar dados válidos

# "plain" schemas usados como um fix para agrupamentos recursivos em schemas
# que contém relacionamentos


class PlainExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=False)
    type = fields.Str(required=True)


class PlainVideoSchema(Schema):
    id = fields.Int(dump_only=True)
    yt_id = fields.Str(required=True)
    title = fields.Str(required=True)


class ExerciseUpdateSchema(Schema):
    name = fields.Str(required=False)
    type = fields.Str(required=False, nullable=True)


class ExerciseSchema(PlainExerciseSchema):
    videos = fields.List(fields.Nested(PlainVideoSchema(), dump_only=True))


class VideoSchema(PlainVideoSchema):
    exercises = fields.List(fields.Nested(PlainExerciseSchema()))


class VideoAndExerciseSchema(Schema):
    exercise = fields.Nested(ExerciseSchema)
    video = fields.Nested(VideoSchema)


class ExerciseLogSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    exercises = fields.List(
        fields.Nested(PlainExerciseSchema()), dump_only=True
    )


# load_only -> receiving data from client
# dump_only -> sending data to client
