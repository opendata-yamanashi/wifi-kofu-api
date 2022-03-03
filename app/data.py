from pathlib import Path
from download import Download
FILEURL = "https://www.city.kofu.yamanashi.jp/joho/opendata/shisetsu/documents/freespot_20200401.csv"
import pandas as pd
import neologdn
from datetime import datetime

class Kofu_wifi():
    BASE_DIR = Path(__file__).absolute().parent.parent
    DATA_DIR = BASE_DIR / "data"

    def __init__(self):
        if not self.DATA_DIR.exists():
            self.DATA_DIR.mkdir()
        
        d = Download(FILEURL, self.DATA_DIR)
        d.download()
        self.fname = self.DATA_DIR / d.name
        self.version = datetime.now().strftime("%Y%m%d")
    
    def create_df(self):
        df = pd.read_csv(self.fname, encoding="sjis", index_col=0)
        df = df.fillna("NoData")
        df.columns = [neologdn.normalize(i) for i in df.columns]
        def replace_n(st):
            return str(st).replace("\n"," ")
        df = df.applymap(replace_n)
        self.df = df

    def get_version(self):
        return self.version

    def query(self, keywords):
        return self.df.loc[self.df["住所"].str.contains(keywords) | self.df["施設名"].str.contains(keywords)]


if __name__ == "__main__":
    kf = Kofu_wifi()
    df = kf.create_df()
    