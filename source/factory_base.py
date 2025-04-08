# https://factoryboy.readthedocs.io/en/stable/orms.html#factory.alchemy.SQLAlchemyModelFactory
import factory.fuzzy
from source.model_base import *
import factory

# https://factoryboy.readthedocs.io/en/stable/orms.html#factory.alchemy.SQLAlchemyModelFactory
factory_session = scoped_session(sessionmaker(bind=engine))


class SampleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Sample
        sqlalchemy_session = factory_session   # the SQLAlchemy session object

    str_a = factory.fuzzy.FuzzyText(
        prefix="str_a_",
        length=10
    )
    str_b = factory.fuzzy.FuzzyText(
        prefix="str_b_",
        length=10
    )


class SampleChildFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = SampleChild
        sqlalchemy_session = factory_session   # the SQLAlchemy session object

    parent_id: int

    str_c = factory.fuzzy.FuzzyText(
        prefix="str_c_",
        length=10
    )
    str_d = factory.fuzzy.FuzzyText(
        prefix="str_d_",
        length=10
    )


if __name__ == "__main__":

    orms: list[Sample] = SampleFactory.create_batch(10)
    factory_session.add_all(orms)
    factory_session.commit()
    for i in range(10):
        children: list[SampleChild] = SampleChildFactory.create_batch(
            10,
            parent_id=orms[i].id
        )
        factory_session.add_all(children)
        factory_session.commit()

    res = factory_session.scalars(select(SampleChild).limit(
        100).order_by(SampleChild.created_at.desc())).all()
    for r in res:
        print(r.__dict__)
