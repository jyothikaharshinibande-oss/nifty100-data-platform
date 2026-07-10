from src.screener.engine import ScreenerEngine


def test_quality_compounder():

    engine = ScreenerEngine()

    df = engine.run("quality_compounder")

    assert len(df) > 0

    assert (df["roe"] > 15).all()

    assert (df["debt_equity"] < 1).all()

    print("Quality Compounder Passed")

    engine.close()


if __name__ == "__main__":
    test_quality_compounder()