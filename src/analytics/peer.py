import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"


class PeerEngine:

    def __init__(self):

        self.conn = sqlite3.connect(DB_PATH)

    def load_data(self):

        query = """

        SELECT

            pg.peer_group_name,

            pg.company_id,

            fr.year,

            fr.return_on_equity_pct,

            fr.debt_to_equity,

            fr.operating_profit_margin_pct,

            fr.asset_turnover,

            fr.free_cash_flow_cr,

            fr.interest_coverage

        FROM peer_groups pg

        INNER JOIN financial_ratios fr

        ON pg.company_id = fr.company_id

        """

        return pd.read_sql(query, self.conn)

    def calculate_percentile(self, df, column, inverse=False):

        result = []

        for group, group_df in df.groupby("peer_group_name"):

            ranks = group_df[column].rank(pct=True)

            if inverse:
                ranks = 1 - ranks

            temp = group_df.copy()

            temp["metric"] = column

            temp["value"] = temp[column]

            temp["percentile_rank"] = ranks

            result.append(temp)

        return pd.concat(result)

    def save_metric(self, df):

        output = df[
            [
                "company_id",
                "peer_group_name",
                "metric",
                "value",
                "percentile_rank",
                "year",
            ]
        ]

        output.to_sql(
            "peer_percentiles",
            self.conn,
            if_exists="append",
            index=False,
        )

    def run(self):

        df = self.load_data()

        metrics = [

            ("return_on_equity_pct", False),

            ("operating_profit_margin_pct", False),

            ("asset_turnover", False),

            ("free_cash_flow_cr", False),

            ("interest_coverage", False),

            ("debt_to_equity", True),

        ]

        self.conn.execute("DELETE FROM peer_percentiles")

        self.conn.commit()

        for metric, inverse in metrics:

            ranked = self.calculate_percentile(
                df,
                metric,
                inverse
            )

            self.save_metric(ranked)

        print("Peer Percentiles Generated Successfully")

        self.conn.close()


if __name__ == "__main__":

    PeerEngine().run()