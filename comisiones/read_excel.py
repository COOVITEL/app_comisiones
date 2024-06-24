import pandas as pd
from typing import Optional

def readExcel(name: str, file: str, asesor: Optional[str] = None, columns: list = [], archive: str = None) -> dict:
    pf = pd.read_excel(f"media/{archive}",
                       sheet_name=file,
                       usecols=columns,
                       na_values=[" "])
    pf.fillna("", inplace=True)
    
    if asesor is not None:
        dates = pf.loc[pf[asesor] == name].to_dict(orient="records")
    else:
        dates = pf.to_dict(orient="records")
    
    return dates