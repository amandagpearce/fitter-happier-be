from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from db import db
from schemas import TagSchema, TagAndExerciseSchema
from models import TagModel, ExercisesModel


blp = Blueprint("Tags", "tags", description="Operações com tags")


@blp.route("/tag")
class TagsInStore(MethodView):
    # @blp.response(200, TagSchema(many=True))
    # def get(self, exercise_id):
    #     exercises = ExercisesModel.query.get_or_404(exercise_id)

    #     return exercises.tags.all()  # lazy="dynamic" means 'tags' is a query

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(
        self, tag_data
    ):  # creates tag - CHANGE SO IT'S ADDED TO EXERCISE AND NOT STORE
        if TagModel.query.filter(
            TagModel.user_id == tag_data["user_id"],
            TagModel.name == tag_data["name"],
        ).first():
            abort(
                400,
                message="Tag com esse nome já existe nesse usuario.",
            )

        tag = TagModel(**tag_data)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return tag


@blp.route("/exercise/<int:item_id>/tag/<int:tag_id>")  # links items + tags
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ExercisesModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if item.user_id == tag.user_id:
            item.tags.append(tag)  # uses the secondary table item_tags,
            # sqlalchemy makes sure the item model will automatically do the
            # changes it needs
        else:
            abort(500, message="Tag e item devem pertencer ao mesmo usuario")

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Ocorreu um erro ao inserir a tag")

        return tag

    @blp.response(200, TagAndExerciseSchema)
    def delete(self, item_id, tag_id):  # un-links items + tags
        item = ExercisesModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)  # working with the secondary table item_tags,
        # sqlalchemy makes sure the item model will automatically do the
        # changes it needs

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Ocorreu um erro ao remover item da tag")

        return {"message": "Item removido da tag", "item": item, "tag": tag}


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    # return tag
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    # delete tag
    @blp.response(  # main response
        202,
        description="Deleta a tag se nenhum item está ligado a ela",
        example={"message": "tag deletada"},
    )
    @blp.alt_response(  # alternative response
        404, description="Tag não encontrada"
    )
    @blp.alt_response(  # alternative response
        400,
        description="""Resposta caso a tag esteja associada um ou mais itens.
        Nesse caso a tag não é deletada.""",
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:  # if there are no items associated with the tag
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deletada"}
        abort(  # abort in case there are items associated
            400,
            message="""Não é possível deletar a tag. Certifique-se que não há
            nenhum item atrelado a ela""",
        )

        return tag
