import os
import pandas as pd
if not os.path.exists("users.csv"):
    pd.DataFrame(
        columns=["username", "password"]
    ).to_csv("users.csv", index=False)