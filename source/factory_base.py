# https://factoryboy.readthedocs.io/en/stable/orms.html#factory.alchemy.SQLAlchemyModelFactory
import factory.fuzzy
from source.model_base import *
import factory

# https://factoryboy.readthedocs.io/en/stable/orms.html#factory.alchemy.SQLAlchemyModelFactory
session = scoped_session(sessionmaker(bind=engine))


class SampleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Sample
        sqlalchemy_session = session   # the SQLAlchemy session object

    str_a = factory.fuzzy.FuzzyText(
        prefix="str_a_",
        length=10
    )


if __name__ == "__main__":

    orms = SampleFactory.create_batch(100)
    session.add_all(orms)
    session.commit()

    res = session.scalars(select(Sample).limit(100).order_by(Sample.created_at.desc())).all()
    for r in res:
        print(r.__dict__)
