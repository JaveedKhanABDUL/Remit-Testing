# REMIT XML Report (Standard Contracts – Continuous) – Test Cases

Source: `REMIT_XML_report_mapping_standard_contracts_Continuous.xlsx` (sheet *REMIT-ELCOM XML mapping*).
Abbreviations: **CDB** = Continuous DB, **RDB** = REMIT DB, **CCDB** = Customer Center DB.
Common precondition: a REMIT XML file is generated for a known set of continuous orders/trades with known source data in CDB/RDB/CCDB.

Priority: P1 = Mandatory tag, P2 = Conditionally required, P3 = Optional.

## 1. Header / Contract list (`REMITTable1`, `contractList`)

| ID | Tag | Scenario | Steps | Expected result | Pri |
|---|---|---|---|---|---|
| TC-001 | REMITTable1 | XML header | Generate file, inspect first lines | `<?xml version="1.0" encoding="UTF-8"?>`; root `REMITTable1` with namespace `http://www.acer.europa.eu/REMIT/REMITTable1_V3.xsd`; file validates against that XSD | P1 |
| TC-002 | REMITTable1 | XSD version change | Change configured XSD version, regenerate | Header namespace/URL reflects the new XSD | P2 |
| TC-003 | reportingEntityID | Value from template | Compare tag with `RDB.TEMPLATE.TPL_RRM_CODE` | Values equal; tag present and non-empty | P1 |
| TC-004 | ace | Type of ID | Inspect tag | Populated (type of reporting entity ID); present | P1 |
| TC-005 | contractId | XBID contract | Report an XBID contract | Format `SIDC_[Short Trading modality]_[SIDC code]_[Short market segment]_[Short Delivery Area]_[Delivery period]` | P1 |
| TC-006 | contractId | Local / GOPACS contract | Report a local and a GOPACS contract | Format follows the structure described in the mapping document for each | P1 |
| TC-007 | contractName | XBID / local / GOPACS | Compare with `RDB.CO_CONTRACT.COC_CONTRACTNAME` | Matches DB value, e.g. `SIDC_CO_EPEX_SPOT_[Market Area]_[Market Segment]_[Trading Modality]_[Duration]` for XBID | P1 |
| TC-008 | contractType | Continuous | Inspect tag | Always `CO` | P1 |
| TC-009 | energyCommodity | Electricity | Inspect tag | Always `EL` | P1 |
| TC-010 | settlementMethod | Physical | Inspect tag | Always `P` | P1 |
| TC-011 | organisedMarketPlaceIdentifier / mic / ace | OMP from template | Compare type with `TPL_OMPTYPE`, value with `TPL_OMPCODE` | Type and value match template (type appears as `mic` or `ace` element accordingly) | P1 |
| TC-012 | contractTradingHours | Continuous market | Inspect tag | Always `00:00Z/24:00Z` | P1 |
| TC-013 | lastTradingDatetime | Same-day closure | Contract with closure offset configured (`COC_TRADINGCLOSURE`) | Value = delivery start − closure offset, in ISO 8601 UTC | P2 |
| TC-014 | lastTradingDatetime | Day-after market | Contract with `AMC_dayoffset` > 0 (e.g. NL closes day after delivery 08:30 local) | Date shifted by dayoffset to local closing time, converted to UTC | P2 |
| TC-015 | lastTradingDatetime | DST change | Contract on a DST switch day | UTC value correct across DST | P2 |
| TC-016 | deliveryPointOrZone | EIC code | Compare with `RDB.AREA.AREA_EICCODE` for the delivery area | EIC matches the configured area; one value per configured EIC | P1 |
| TC-017 | deliveryStartDate | Date only | Compare with `CDB.ORDERS.ORD_DELIVERY_START` | ISO 8601 date (UTC) without time part | P1 |
| TC-018 | deliveryEndDate | Date only | Compare with `ORD_DELIVERY_END` | ISO 8601 date (UTC), no time part | P1 |
| TC-019 | duration | 60 min contract | `COC_DURATION = '60min'` | `H` | P1 |
| TC-020 | duration | 30 min / 15 min contract | `COC_DURATION <> '60min'` | `N` | P1 |
| TC-021 | loadType | Load type mapping | Compare with `COC_LOADTYPE` | Matches DB | P1 |
| TC-022 | loadDeliveryStartTime | Time format | Compare with `ORD_DELIVERY_START` | `HH:MM:SS` UTC (time part only) | P1 |
| TC-023 | loadDeliveryEndTime | Time format | Compare with `ORD_DELIVERY_END` | `HH:MM:SS` UTC (time part only) | P1 |

## 2. OrderList / OrderReport

| ID | Tag | Scenario | Steps | Expected result | Pri |
|---|---|---|---|---|---|
| TC-101 | RecordSeqNumber | Sequence | Report several orders | Integers starting at 1, incrementing, no gaps/duplicates; no non-integer values | P1 |
| TC-102 | idOfMarketParticipant + type (fields 1,2) | Direct member | Order by direct member | Value = `CCDB.View_Reporting.ClientReportingCode` for `ORDERS.MEM_PKEY`; code type populated | P1 |
| TC-103 | idOfMarketParticipant + type | Indirect member (PCT) | Order by indirect member | Reporting code taken from the member reference per mapping rules; type correct | P1 |
| TC-104 | traderIdForOrganisedMarket | Concatenation | Compare with `ORDERS.ORD_MEMBER` & `ORDER_REVISION.ORR_USER_CODE` | Member ID concatenated with user code as specified | P1 |
| TC-105 | tradingCapacity | Direct member / PM | Direct member and PM order | `P`; `beneficiaryIdentification` not present | P1 |
| TC-106 | tradingCapacity | Indirect member (PCT) | Order from PCT per `view_sponsorship` | `A`; `beneficiaryIdentification` block populated | P1 |
| TC-107 | beneficiaryIdentification (fields 8, 9) | Indirect member | Inspect block | ID from `ClientReportingCode`, type of code present | P2 |
| TC-108 | buySellIndicator | Buy / Sell | Orders with `ORD_SIDE` buy and sell | Value matches `ORD_SIDE` mapping | P1 |
| TC-109 | uniqueOrderIdentifier | UOI format | Compare with `BDB_PKEY` + `ORD_INITIALID` | Prefix (business DB code) + trading system ID per mapping; unique across orders | P1 |
| TC-110 | uniqueOrderIdentifier | Modified order | Order with multiple revisions | Same UOI across revisions | P1 |
| TC-111 | previousOrderIdentifier | Optional | Order with and without predecessor | Tag follows N/A rule; absent when not applicable | P3 |
| TC-112 | orderType | Linked FOK | `ORD_BASKET_EXEC_RESTRICTION='LINKED'` and `EXECUTION_RESTRICTION='FOK'` | `LIN` | P1 |
| TC-113 | orderType | Block | `ISBLOCK=1`, not linked/FOK | `BLO` | P1 |
| TC-114 | orderType | Block + linked FOK | Both conditions met | `LIN` (linked rule takes precedence) | P1 |
| TC-115 | orderType | Plain | None of the conditions met | `LIM` | P1 |
| TC-116 | orderCondition | Iceberg | `ORD_ORDER_TYPE='I'` (any execution restriction) | `HVO` | P2 |
| TC-117 | orderCondition | Predefined block IOC | `PRO_ISPREDEFINEDBLOCK=1` and restriction `IOC` | `FAK` | P2 |
| TC-118 | orderCondition | FOK | Restriction `FOK` | `FOK` | P2 |
| TC-119 | orderCondition | AON | Restriction `AON` | `AON` | P2 |
| TC-120 | orderCondition | No restriction | None apply | Tag omitted | P2 |
| TC-121 | orderStatus | Status mapping | For each `ORR_ACTION_CODE` in `CO_ACTIONCODECONFIGURATION` | Status = `ACC_REMITSTATUS` for matching `ACC_M7CODEACTION` | P1 |
| TC-122 | orderStatus | Unmapped action code | Revision with unconfigured action code | Handled per config (error/skip); no wrong status emitted | P2 |
| TC-123 | minimumExecuteVolume | Value/unit | Order with min. execute volume | Value numeric, unit populated; block absent otherwise | P2 |
| TC-124 | undisclosedVolume.value | Iceberg | Iceberg order | `ORR_TOTAL_REMAINING_QUANTITY − ORR_QUANTITY` | P2 |
| TC-125 | undisclosedVolume.unit | Unit | Inspect | `MW` | P2 |
| TC-126 | orderDuration.duration | GTD | `ORR_VALIDITY_RESTRICTION='GTD'` | `GTT` | P1 |
| TC-127 | orderDuration.duration | GFS / NON | `'GFS'` and `'NON'` | `SES` | P1 |
| TC-128 | expirationDateTime | GTD | GTD order | `ORR_VALIDITY_TIME` in UTC | P1 |
| TC-129 | expirationDateTime | Non-GTD | GFS/NON order | Tag not displayed | P1 |
| TC-130 | contractInfo.contractId / mic / ace | Same as contract | Compare with contract list | Matches TC-005..TC-011 | P1 |
| TC-131 | transactionTime | UTC conversion | Compare with `ORR_TRANSACTION_TIME` | ISO 8601 UTC (e.g. ends in `Z`); local time converted correctly incl. DST | P1 |
| TC-132 | linkedOrderId | Basket (LIN) | Linked FOK basket order | Format `[BDB_PKEY]_B_[Basket ID]` from `ORD_BASKETID` | P2 |
| TC-133 | linkedOrderId | No basket | Non-linked order | Tag absent | P2 |
| TC-134 | priceDetails.price | Price | Compare with `ORR_PRICE` | Numeric value matches; negative prices preserved | P2 |
| TC-135 | priceDetails.priceCurrency | Currency | Compare with `CURRENCY.CUR_ISO_CODE` via `ORDERS.CUR_PKEY` | ISO currency code matches | P2 |
| TC-136 | quantity.value | Partial match | `orderStatus = 'MAC'` | Value from `ORR_EXECUTED_QUANTITY` | P2 |
| TC-137 | quantity.value | Other status | Any status other than `MAC` | Value from `ORR_QUANTITY` | P2 |
| TC-138 | quantity.unit | Unit | Inspect | `MW` | P2 |
| TC-139 | totalNotionalContractQuantity.value | 60 min product, 1 hour | Quantity × periods | = `ORR_QUANTITY` × (duration/60) × instruments; correct | P2 |
| TC-140 | totalNotionalContractQuantity.value | Multi-instrument, 15 min | Delivery span of several instruments | Quantity × (15/60) × number of instruments | P2 |
| TC-141 | totalNotionalContractQuantity.value | Rounding | Result with > 5 decimals / ≤ 5 decimals | Rounded to max 5 decimals; no rounding otherwise | P2 |
| TC-142 | totalNotionalContractQuantity.unit | Unit | Inspect | `MW` | P2 |
| TC-143 | priceTimeIntervalQuantityDetails | Interval fields | Inspect block (intervalStart/EndTime, quantity, unit, value, currency) | Conforms to XSD; per mapping (N/A mapping — confirm expected population with business) | P3 |
| TC-144 | actionType | New | First revision of an order | `N` | P1 |
| TC-145 | actionType | Modify | Member modifies order | `M` | P1 |
| TC-146 | actionType | Cancel | Member deletes order | `C` | P1 |
| TC-147 | actionType | Error (cancellation task) | Run LISE cancellation task | All records in the generated file have `E` | P1 |
| TC-148 | actionType | System deletion | Order expired/deleted by system | Not reported | P1 |
| TC-149 | extra | Non SEMOpx/GOPACS | Order on other market | Tag NULL / not present | P2 |
| TC-150 | extra | SEMOpx | SEMOpx order | Format `BidUnitIDxxx==Yes;BidUnitIDxxx==Yes` | P2 |
| TC-151 | extra | GOPACS | GOPACS order | Format per mapping document | P2 |

## 3. TradeList / TradeReport

| ID | Tag | Scenario | Steps | Expected result | Pri |
|---|---|---|---|---|---|
| TC-201 | RecordSeqNumber | Sequence | Report several trades | Integers starting at 1, incrementing | P1 |
| TC-202 | idOfMarketParticipant + type (fields 1,2) | Direct / indirect | Trades from both member types | Value from `ClientReportingCode` via `MEM_PKEY`; type populated | P1 |
| TC-203 | traderIdForOrganisedMarket | Concatenation | Compare with `TRADE_LEG.TRL_MEMBER` & `TRL_USER_CODE` | Concatenated correctly | P1 |
| TC-204 | tradingCapacity | Direct / PM | Trade of direct member and PM | `P`, no beneficiary block | P1 |
| TC-205 | tradingCapacity | PCT | Trade of indirect member | `A`, beneficiary block filled | P1 |
| TC-206 | beneficiaryIdentification (8, 9) | Indirect member | Inspect | Value from `ClientReportingCode` via `TRADE_LEG.CC_MEM_PKEY`; type present | P2 |
| TC-207 | buySellIndicator | Buy / Sell | Compare with `TRL_SIDE` | Matches | P1 |
| TC-208 | aggressor | Value present | `TRL_AGGRESSOR` populated | Value reported | P2 |
| TC-209 | aggressor | Null | `TRL_AGGRESSOR` null | Tag does not appear | P2 |
| TC-210 | contractInfo.contractId / mic / ace | Consistency | Compare with contract list | Same values; mandatory | P1 |
| TC-211 | transactionTime | UTC conversion | Compare with `TRADE_REVISION.TRR_REVISION_TIME` | ISO 8601 UTC | P1 |
| TC-212 | uniqueTransactionIdentifier | XBID vs local | Report both | Prefix + trading system ID; format differs per XBID/local as specified | P1 |
| TC-213 | additionalUtiInfo | XBID trade | XBID trade | Present with `XBID` | P3 |
| TC-214 | additionalUtiInfo | Local trade | Local trade | Sub-tag does not appear | P3 |
| TC-215 | linkedOrderId | Local trade | Local trade | `ORD_INITIALID` related to `TRL_ORDERID` (equals order UOI) | P2 |
| TC-216 | linkedOrderId | Remote trade | Remote trade | `ORR_REMOTE_ID` related to `TRL_ORDERID` | P2 |
| TC-217 | linkedOrderId | OTC | `TRADE.TRA_ISOTC = 1` | `NA` | P2 |
| TC-218 | priceDetails.price | Price | Compare with `TRL_PRICE` | Matches (incl. negative) | P2 |
| TC-219 | priceDetails.priceCurrency | Currency | Compare with `CUR_ISO_CODE` via `TRADE_LEG.CUR_PKEY` | Matches | P2 |
| TC-220 | notionalAmount | Calculation | Price × quantity × periods × instruments | Equals expected, rounded to max 5 decimals if more | P2 |
| TC-221 | notionalCurrency | Currency | Compare | Same ISO code as priceCurrency | P2 |
| TC-222 | quantity.value | Quantity | Compare with `TRL_QUANTITY` | Matches | P2 |
| TC-223 | quantity.unit | Unit | Inspect | `MW` (mandatory) | P1 |
| TC-224 | totalNotionalContractQuantity.value | Calculation | `TRL_QUANTITY` × (duration/60) × instruments (from `TRA_DELIVERY_*` and `PRO_INSTRUMENT_CLASS`) | Matches; max 5 decimals | P1 |
| TC-225 | totalNotionalContractQuantity.unit | Unit | Inspect | `MW` | P1 |
| TC-226 | actionType | New | New trade | `N` | P1 |
| TC-227 | actionType | Cancelled/recalled | `TRR_STATUS` = `RGRA` or `CNCL` | `C` | P1 |
| TC-228 | actionType | Error (cancellation task) | Run LISE cancellation task | All records `E` | P1 |
| TC-229 | extra | Non SEMOpx/GOPACS | Other market trade | NULL / absent | P2 |
| TC-230 | extra | SEMOpx / GOPACS | SEMOpx and GOPACS trades | Format per mapping document | P2 |

## 4. Cross-cutting

| ID | Scenario | Expected result |
|---|---|---|
| TC-301 | Full file XSD validation (orders and trades) | Passes `REMITTable1_V3.xsd` |
| TC-302 | All Mandatory tags present in every record | No missing mandatory tags |
| TC-303 | Conditionally required tags | Present only when their condition applies |
| TC-304 | Empty order list / trade list | File still valid; no empty report records |
| TC-305 | Large volume (many orders/trades) | Sequence numbers unique, no data loss or duplicates |
| TC-306 | All timestamps | ISO 8601 UTC |
| TC-307 | Multiple delivery areas / EICs | Each area mapped to its configured EIC |
| TC-308 | Re-run for same period | Output identical/idempotent per configured behaviour |
