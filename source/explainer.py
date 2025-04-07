from sqlalchemy import Select
from sqlalchemy.dialects import postgresql
import os
from source.model_base import *

OUT_DIR = "out/query_explain"


def explain_analyze(
    query: Select,
    label: str = None
) -> str:
    sql = str(query.compile(engine, postgresql.dialect(), compile_kwargs={"literal_binds": True}))
    query_exp = f"explain analyze {sql}"
    try:
        with Session(engine) as s:
            res = s.execute(text(query_exp)).all()
        query_text = "\n".join([str(r[0]) for r in res])
    except Exception as e:
        print(e)
        query_text = "failed explain"
    print(query_text)

    out_dir = f"{OUT_DIR}"
    if label:
        out_dir += f"/{label}"

    os.makedirs(out_dir, exist_ok=True)

    with open(f"{out_dir}/explain.sql", "w", encoding="utf-8") as f:
        f.write(query_exp)
    with open(f"{out_dir}/execute.sql", "w", encoding="utf-8") as f:
        f.write(sql)
    with open(f"{out_dir}/result.txt", "w", encoding="utf-8") as f:
        f.write(query_text)


if __name__ == "__main__":
    explain_analyze(
        select(Sample).limit(100).order_by(Sample.created_at.desc()),
        "sample"
    )
