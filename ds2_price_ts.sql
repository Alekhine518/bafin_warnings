declare @isin varchar(12) = 'CA8433031082';
declare @start date = '20170101';
declare @end date = getdate();

with
info as
(
select	cqi.*, 
		ic.ISIN,
		ic.ISIN2,
		eqi.ExchIntCode,
		eqi.IsPrimExchQt,
		eqi.MIC,
		eqi.MICDesc
from DS2CtryQtInfo cqi
join DS2ISINChg ic
	on cqi.DsSecCode = ic.DsSecCode
join DS2ExchQtInfo eqi
	on cqi.InfoCode = eqi.InfoCode
where ISIN = @isin
),
price as
(
select * from
(
select * from DS2PrimQtPrc
	union
select * from Ds2ScdQtPrc
) x
where	InfoCode in (select InfoCode from info) and
		MarketDate between @start and @end
)

select	info.*,
		price.MarketDate,
		price.Close_,
		price.ISOCurrCode,
		price.VWAP,
		price.Volume,
		price.Ask,
		price.Bid,
		price.Open_,
		price.High,
		price.Low,
		price.ConsolVol
from info
left join price
	on	info.InfoCode = price.InfoCode and
		info.ExchIntCode = price.ExchIntCode
