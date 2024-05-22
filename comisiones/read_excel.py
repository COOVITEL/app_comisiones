import pandas as pd


def readExcel(name: str, file: str, asesor: str, columns: list, archive: str) -> dict:
    """"""
    pf = pd.read_excel(f"media/{archive}",
                       sheet_name=file,
                       usecols=columns,
                       na_values=[" "])
    pf.fillna("", inplace=True)
    dates = pf.loc[pf[asesor] == name].to_dict(orient="records")
    return dates
