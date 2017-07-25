import pandas as pdimport jss_data as jssimport picklefrom datetime import datetime as dt, timedelta
def get_price_ts_basic(isin, dt_start, dt_end):
    s_start = dt_start.strftime('%Y%m%d')    s_end = dt_end.strftime('%Y%m%d')
    sql = '''    with    info as    (    select  cqi.*,            ic.ISIN,            ic.ISIN2,            eqi.ExchIntCode,            eqi.IsPrimExchQt,            eqi.MIC,            eqi.MICDesc    from DS2CtryQtInfo cqi    join DS2ISINChg ic        on cqi.DsSecCode = ic.DsSecCode    join DS2ExchQtInfo eqi        on cqi.InfoCode = eqi.InfoCode    where ISIN = '{0}'    ),    price as    (    select * from    (    select * from DS2PrimQtPrc        union    select * from Ds2ScdQtPrc    ) x    where   InfoCode in (select InfoCode from info) and            MarketDate between '{1}' and '{2}'    )
    select  info.*,            price.MarketDate,            price.Close_,            price.ISOCurrCode,            price.VWAP,            price.Volume,            price.Ask,            price.Bid,            price.Open_,            price.High,            price.Low,            price.ConsolVol    from info    left join price        on  info.InfoCode = price.InfoCode and            info.ExchIntCode = price.ExchIntCode    '''    sql = sql.format(isin, s_start, s_end)    con = jss.sql_cnxn('qad')    df = pd.read_sql(sql, con, parse_dates=['MarketDate'])    return df
def get_prices_ts_window(isin, dt_event, ante, post):
    dt_start = dt_event - timedelta(weeks=ante)    dt_end = dt_event + timedelta(weeks=post)    df = get_price_ts_basic(isin, dt_start, dt_end)    return df
def main():
    # Load dataframe with cases.    file_path = r'W:\A\AMS\Team\WISE\99_dev\bafin_warnings\bafin_warnings.xlsx'    df = pd.read_excel(file_path, header=0)
    # For each case query ds2 prices.    frames = dict()    for idx, row in df.iterrows():        isin = row['ISIN']        ts_event = row['DATE']
        df = get_prices_ts_window(isin, ts_event, 5, 5)        frames[isin] = df
    # Pickle resulting dictionary of isins and dataframes.    pickle.dump(frames, open('bafin_get_price_ts.p', 'wb'))
if __name__ == "__main__":    main()
