from src.screener.engine import ScreenerEngine


def quality_compounder():
    engine = ScreenerEngine()
    df = engine.run("quality_compounder")
    engine.close()
    return df


def value_pick():
    engine = ScreenerEngine()
    df = engine.run("value_pick")
    engine.close()
    return df


def growth_accelerator():
    engine = ScreenerEngine()
    df = engine.run("growth_accelerator")
    engine.close()
    return df


def dividend_champion():
    engine = ScreenerEngine()
    df = engine.run("dividend_champion")
    engine.close()
    return df


def debt_free_blue_chip():
    engine = ScreenerEngine()
    df = engine.run("debt_free_blue_chip")
    engine.close()
    return df


def turnaround_watch():
    engine = ScreenerEngine()
    df = engine.run("turnaround_watch")
    engine.close()
    return df


def run_all_presets():

    presets = {
        "quality_compounder": quality_compounder,
        "value_pick": value_pick,
        "growth_accelerator": growth_accelerator,
        "dividend_champion": dividend_champion,
        "debt_free_blue_chip": debt_free_blue_chip,
        "turnaround_watch": turnaround_watch,
    }

    results = {}

    print("=" * 65)
    print("SPRINT 3 - PRESET SCREENER SUMMARY")
    print("=" * 65)

    for name, func in presets.items():

        df = func()

        results[name] = df

        print(f"{name:25} {len(df):5} companies")

    print("=" * 65)

    return results


if __name__ == "__main__":

    run_all_presets()