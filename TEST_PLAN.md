# REMIT XML Test Plan – Continuous Market (Standard Contracts)

Scope: manual validation of the REMIT Table 1 XML report against
`REMIT_XML_report_mapping_standard_contracts_Continuous.xlsx`.
Basis: no daily activity was available (no recent commits/PRs/sessions), so this plan is derived from the only
content in the repo, the mapping spreadsheet. Extend it with the day's changes once supplied.

## Environment and data
- REMIT DB, Continuous DB, Customer Center DB access; generated XML for a known trading date.
- Validate each file against the XSD `REMITTable1_V3.xsd`.
- Data set: new / modified / cancelled / partially executed / fully executed orders; iceberg (undisclosed volume) orders;
  basket (linked) orders; XBID cross-border trades; direct member and non-direct member (trading capacity) cases;
  60/30/15 min contracts; base/peak/block load types.

## Scenarios (by priority)

### P1 – Mandatory fields and schema (High risk)
| ID | Area | Scenario | Expected |
|----|------|----------|----------|
| T1 | Schema | XML validates against XSD; header/namespace correct | No schema errors |
| T2 | Mandatory tags | All "Mandatory" tags present in ContractList, OrderReport, TradeReport | None missing/empty |
| T3 | Header | reportingEntityID/ace equals `TEMPLATE.TPL_RRM_CODE` | Match |
| T4 | Hard-coded | contractType=CO, energyCommodity=electricity, settlementMethod=physical, unit=MW | Exact values |
| T5 | Trading hours | contractTradingHours = 00:00Z/24:00Z | Exact |

### P1 – Orders (High risk)
| ID | Scenario | Expected |
|----|----------|----------|
| T6 | uniqueOrderIdentifier maps to BDB_PKEY / ORD_INITIALID | Match DB |
| T7 | orderType per ORD_ORDER_TYPE (3 values); orderCondition only when type = 'I' | Correct mapping; absent otherwise |
| T8 | orderStatus from ACC_REMITSTATUS; actionType (N/M/C/E) from ACC_REMITACTIONTYPE | Match config for each lifecycle event |
| T9 | Iceberg order: undisclosedVolume = total – displayed | Correct calculation |
| T10 | orderDuration/expirationDateTime only for orders with validity time | Present only when applicable |
| T11 | price, priceCurrency (ISO code), quantity from ORR_PRICE/ORR_EXECUTED_QUANTITY | Match DB |
| T12 | transactionTime ISO8601 UTC with required precision | Format valid |
| T13 | linkedOrderId = ORD_BASKETID for basket orders; absent otherwise | Correct |
| T14 | RecordSeqNumber starts at 1, integer, sequential | Correct |
| T15 | traderIdForOrganisedMarket = ORD_MEMBER & ORR_USER_CODE | Match |

### P1 – Trades (High risk)
| ID | Scenario | Expected |
|----|----------|----------|
| T16 | UTI built with correct prefix; additionalUtiInfo for XBID trades | Correct |
| T17 | price, quantity from TRL_PRICE / TRL_QUANTITY | Match DB |
| T18 | notionalAmount = price × quantity × periods; notionalCurrency | Correct calculation |
| T19 | totalNotionalContractQuantity = volume × number of periods | Correct |
| T20 | buySellIndicator (TRL_SIDE), aggressor (TRL_AGGRESSOR; absent when null) | Correct |
| T21 | linkedOrderId equals the order's uniqueOrderIdentifier | Cross-file match |
| T22 | tradingCapacity "P" for direct members, "A" otherwise | Correct |

### P2 – Contracts
| ID | Scenario | Expected |
|----|----------|----------|
| T23 | contractId/Name follow XBID/SIDC naming; consistent in Contract, Order, Trade | Consistent |
| T24 | duration mapping (60min → H, etc.); loadType from COC_LOADTYPE | Correct |
| T25 | deliveryStart/EndDate and loadDeliveryStart/EndTime from ORD_DELIVERY_* (UTC) | Correct, DST days (23/25h) included |
| T26 | deliveryPointOrZone EIC from AREA_EICCODE | Correct |
| T27 | lastTradingDatetime when conditionally required | Present/absent correctly |
| T28 | mic/ace type and value from TPL_OMPTYPE / template | Correct |

### P3 – Negative / edge
| ID | Scenario | Expected |
|----|----------|----------|
| T29 | Day with no orders/trades | Valid XML with empty lists |
| T30 | Missing client reporting code / beneficiary | Conditionally required fields handled, no crash |
| T31 | Optional tags (previousOrderIdentifier, extra) for non-SEMOpx markets | Omitted/NULL |
| T32 | Special characters in names; very large volumes/prices; negative prices | Escaped and valid |
| T33 | Order amended multiple times / cancelled after partial fill | Each revision reported in order |

## Regression focus
Order lifecycle status/action mapping, DST days, XBID trades, and any template/config change.

## Open questions
- Which changes/PRs from the day should be added as targeted scenarios?
- Is the extra tag required only for SEMOpx?
- Target XSD version and ACER priority levels to treat as blocking.

## Out of scope
Non-continuous (auction) markets, non-standard contracts, transport/submission to ACER.
