TICKERS_100 = [
    # US Megacaps & Technology
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "AVGO", "NFLX", "AMD",
    "ADBE", "CRM", "QCOM", "INTC", "IBM", "TXN", "AMAT", "MU", "LRCX", "NOW",
    
    # Financials & Insurance
    "JPM", "V", "MA", "BAC", "WFC", "GS", "MS", "AXP", "BLK", "C",
    "SPGI", "PGR", "CB", "MMC", "ICE", "CME", "USB", "PNC", "TFC", "BK",
    
    # Healthcare & Pharmaceuticals
    "LLY", "UNH", "JNJ", "PFE", "ABBV", "MRK", "TMO", "DHR", "ISRG", "AMGN",
    "ELV", "CVS", "CI", "SYK", "ZTS", "BDX", "BSX", "GILD", "VRTX", "REGN",
    
    # Consumer Goods & Retail
    "WMT", "PG", "HD", "COST", "KO", "PEP", "MCD", "NKE", "SBUX", "TGT",
    "LOW", "CL", "MDLZ", "EL", "GIS", "KHC", "HSY", "STZ", "GIS", "DG",
    
    # Industrials, Energy & Materials
    "XOM", "CVX", "CAT", "GE", "HON", "UNP", "UPS", "RTX", "LMT", "BA",
    "DE", "MMM", "ETN", "LIN", "APD", "SHW", "NEM", "FCX", "SLB", "COP",
    
    # European & International (Yahoo Suffixes)
    "RHM.DE", "ASML.AS", "BMW.DE", "SIE.DE", "SAP.DE", "AIR.PA", "SAN.PA", "OR.PA", 
    "NESN.SW", "NOVN.SW", "ROG.SW", "SHEL.L", "AZN.L", "HSBA.L", "ULVR.L", 
    "BP.L", "RIO.L", "GSK.L", "ENEL.MI", "IBE.MC"
]

ADDITIONAL_TICKERS_100 = [
    # ==========================================
    # 1. SURVIVORSHIP BIAS COUNTERWEIGHTS 
    #    (Historical Laggards, Post-Peak Tech, Turnarounds & Cyclicals)
    # ==========================================
    "WBA",   # Walgreens Boots Alliance (severe retail pharmacy decline)
    "NOK",   # Nokia (telecom lag post-smartphone era)
    "BB",    # BlackBerry (hardware to slow software pivot)
    "LUMN",  # Lumen Technologies (secular wireline/telecom decline)
    "PARA",  # Paramount Global (legacy media linear TV headwinds)
    "PYPL",  # PayPal Holdings (post-pandemic multiple contraction)
    "SQ",    # Block / Square (fintech volatility)
    "ZM",    # Zoom Video (post-pandemic normalization)
    "PTON",  # Peloton Interactive (hardware demand collapse)
    "SNAP",  # Snap Inc. (ad-market cyclicality)
    "PINS",  # Pinterest
    "DOCU",  # DocuSign
    "Roku",  # Roku ("ROKU")
    "ETSY",  # Etsy
    "BYND",  # Beyond Meat (secular adoption pullback)
    "DKNG",  # DraftKings
    "U",     # Unity Software
    "F",     # Ford Motor Company (high capital intensity, cyclical auto)
    "GM",    # General Motors
    "CCL",   # Carnival Corporation (pandemic debt and cruise cyclicality)
    "RCL",   # Royal Caribbean Group
    "DAL",   # Delta Air Lines
    "AAL",   # American Airlines Group
    "UAL",   # United Airlines Holdings
    "BA",    # Boeing (manufacturing and safety execution headwinds)

    # ==========================================
    # 2. EMERGING MARKETS: LATIN AMERICA (South America & Mexico)
    # ==========================================
    "MELI",  # MercadoLibre (Argentina/Brazil) - LatAm e-commerce & fintech
    "VALE",  # Vale SA (Brazil) - Global iron ore mining titan
    "PBR",   # Petrobras (Brazil) - State-backed energy and oil producer
    "NU",    # Nu Holdings (Brazil) - Digital banking disruptor
    "ITUB",  # Itaú Unibanco (Brazil) - Major South American private bank
    "BBD",   # Banco Bradesco (Brazil) - Commercial bank
    "ABEV",  # Ambev SA (Brazil) - Beverage & brewing giant
    "BSBR",  # Banco Santander Brasil
    "SUZ",   # Suzano SA (Brazil) - World's largest wood pulp producer
    "GGB",   # Gerdau SA (Brazil) - Steel producer
    "SID",   # Companhia Siderúrgica Nacional (Brazil) - Steel & mining
    "CX",    # Cemex (Mexico) - Building materials and cement
    "FMX",   # Fomento Económico Mexicano (Mexico) - Beverage/retail
    "AMX",   # América Móvil (Mexico) - Telecom giant
    "BCH",   # Banco de Chile (Chile) - Major commercial bank
    "SQM",   # Sociedad Química y Minera de Chile - Lithium & specialty fertilizers
    "ARCO",  # Arcos Dorados (LatAm) - Largest McDonald's franchise operator globally
    "GLOB",  # Globant (Argentina/LatAm origin) - IT and software engineering
    "DESP",  # Despegar.com (LatAm) - Online travel platform
    "YPF",   # YPF SA (Argentina) - Integrated energy and oil producer
    "BBAR",  # Banco Macro (Argentina) - Regional banking
    "CAAP",  # Corporación América Airports (Argentina/LatAm) - Airport operations
    "VIST",  # Vista Energy (Argentina/Mexico) - Oil and gas exploration
    "PAGS",  # PagSeguro Digital (Brazil) - Fintech and payment solutions
    "CRESY",  # Cresud (Argentina) - Agricultural and real estate enterprise

    # ==========================================
    # 3. EMERGING MARKETS: ASIA-PACIFIC (Greater China, India, Taiwan, Korea)
    # ==========================================
    "TSM",   # Taiwan Semiconductor Manufacturing (Taiwan) - Foundry monopoly
    "BABA",  # Alibaba Group (China) - E-commerce and cloud infrastructure
    "JD",    # JD.com (China) - Direct-sales e-commerce and logistics
    "BIDU",  # Baidu (China) - Search engine and AI initiatives
    "TCEHY", # Tencent Holdings (China) - Gaming and social media ecosystem
    "NTES",  # NetEase (China) - Online gaming and services
    "PDD",   # PDD Holdings (China) - Value e-commerce platform
    "BILI",  # Bilibili (China) - Video and online entertainment
    "NIO",   # NIO Inc. (China) - Electric vehicle manufacturer
    "XPEV",  # XPeng (China) - EV manufacturer
    "LI",    # Li Auto (China) - EREV and EV manufacturer
    "INFY",  # Infosys (India) - IT services and consulting
    "WIT",   # Wipro (India) - Information technology services
    "IBN",   # ICICI Bank (India) - Private sector banking
    "HDB",   # HDFC Bank (India) - Banking and financial services
    "MMYT",  # MakeMyTrip (India) - Online travel services
    "UMC",   # United Microelectronics (Taiwan) - Semiconductor foundry
    "ASX",   # ASE Technology Holding (Taiwan) - Semiconductor packaging/testing
    "PKX",   # POSCO Holdings (South Korea) - Steel manufacturing
    "KB",    # KB Financial Group (South Korea) - Financial holding company
    "SKM",   # SK Telecom (South Korea) - Telecommunications
    "SONY",  # Sony Group (Japan) - Electronics, gaming, and entertainment
    "TM",    # Toyota Motor (Japan) - Automotive manufacturing
    "MUFG",  # Mitsubishi UFJ Financial Group (Japan) - Banking
    "SHEL.L" # (Already captured in your primary list, substituting with:) 
    # Let's use HMC (Honda Motor - Japan) instead
    "HMC",   # Honda Motor (Japan) - Automotive and power equipment

    # ==========================================
    # 4. GLOBAL DEVELOPED MARKETS, CANADA & EUROPEAN LAGGARDS
    # ==========================================
    "SHOP",  # Shopify (Canada) - E-commerce platform software
    "RY",    # Royal Bank of Canada (Canada) - Financials
    "TD",    # Toronto-Dominion Bank (Canada) - Financials
    "BMO",   # Bank of Montreal (Canada) - Financials
    "ENB",   # Enbridge (Canada) - Energy infrastructure and pipelines
    "CNQ",   # Canadian Natural Resources (Canada) - Oil and gas exploration
    "CP",    # Canadian Pacific Kansas City (Canada) - Transcontinental rail
    "FTS",   # Fortis Inc. (Canada) - Regulated electric and gas utility
    "TRI",   # Thomson Reuters (Canada) - Information and software services
    "BN",    # Brookfield Corporation (Canada) - Alternative asset management
    "BAM",   # Brookfield Asset Management (Canada) - Asset management spin-off
    "BHP",   # BHP Group (Australia) - Global resources and mining
    "RIO",   # Rio Tinto (Australia/UK) - Mining and metals
    "VOD",   # Vodafone Group (UK/Europe) - Classic telecom structural laggard/turnaround
    "ORAN",  # Orange SA (France) - European legacy telecom operator
    "TEF",   # Telefónica (Spain) - Telecommunications value trap/restructuring case
    "ENGI.PA", # Engie (France) - Energy utility and transition
    "VNA.DE",  # Vonovia SE (Germany) - Residential real estate / interest rate sensitivity
    "GSK",   # GlaxoSmithKline (UK) - Biopharma
    "BP",    # BP PLC (UK) - Integrated energy
    "DEO",   # Diageo (UK/Global) - Alcoholic beverages multi-year consolidation
    "UL",    # Unilever (UK/Global) - Consumer staples slower growth compounder
    "SNY",   # Sanofi (France) - Healthcare and pharmaceuticals
    "BAYN.DE", # Bayer AG (Germany) - Litigation-heavy conglomerate / cyclical pharma value trap
    "DBK.DE"   # Deutsche Bank AG (Germany) - Banking restructuring and historical volatility

    # ==========================================
    # 1. NORDIC & EUROPEAN DEVELOPED MARKETS
    # ==========================================
    "NOVO-B.CO", # Novo Nordisk (Denmark) - Healthcare & pharmaceuticals giant
    "DSV.CO",    # DSV A/S (Denmark) - Global transport and logistics
    "ORSTED.CO", # Ørsted (Denmark) - Renewable energy / wind power cyclicality
    "MAERSK-B.CO", # A.P. Møller - Mærsk (Denmark) - Shipping & marine logistics
    "EQNR.OL",   # Equinor (Norway) - Integrated energy and oil/gas
    "TEL.OL",    # Telenor (Norway) - Telecommunications
    "ERIC-B.ST", # Ericsson (Sweden) - Telecom infrastructure & equipment laggard/turnaround
    "VOLV-B.ST", # Volvo AB (Sweden) - Commercial vehicles and industrial cyclicals
    "SAND.ST",   # Sandvik (Sweden) - Engineering and mining equipment
    "HEXA-B.ST", # Hexagon AB (Sweden) - Industrial technology and software
    "KNEBV.HE",  # Kone Oyj (Finland) - Elevators and escalators
    "NOKIA.HE",  # Nokia Oyj (Finland primary listing) - Tech laggard
    "NESN.SW",   # Nestlé (Switzerland) - Consumer goods
    "ZURN.SW",   # Zurich Insurance Group (Switzerland) - Insurance
    "ABBN.SW",   # ABB Ltd (Switzerland) - Electrification and automation
    "ENEL.MI",   # Enel SpA (Italy) - Utilities and clean energy
    "ISP.MI",    # Intesa Sanpaolo (Italy) - Commercial banking
    "UCG.MI",    # UniCredit (Italy) - European banking restructuring
    "IBE.MC",    # Iberdrola (Spain) - Renewable energy and utilities
    "SAN.MC",    # Banco Santander (Spain) - Global banking

    # ==========================================
    # 2. ADDITIONAL HISTORICAL LAGGARDS & CYCLICALS
    # ==========================================
    "XRAY",      # Dentsply Sirona (Dental equipment slowdown/valuation compression)
    "PARA",      # Paramount Global (Legacy media headwinds)
    "WBA",       # Walgreens Boots Alliance (Retail pharmacy transformation challenges)
    "CHWY",      # Chewy (Online pet retail post-pandemic growth normalization)
    "TWLO",      # Twilio (Cloud communications growth deceleration)
    "OKTA",      # Okta (Identity management valuation and growth repricing)
    "ZM",        # Zoom Video Communications (Remote work normalization cycle)
    "PTON",      # Peloton Interactive (Hardware demand contraction)
    "DOCU",      # DocuSign (SaaS post-boom normalization)
    "Roku",      # Roku (Connected TV hardware/ad-spend cyclicality)
    "MDB",       # MongoDB (Database software cyclicality)
    "SNOW",      # Snowflake (Cloud data platform growth recalibration)
    "PLTR",      # Palantir Technologies (Data analytics scaling trajectory)
    "U",         # Unity Software (Gaming engine monetization shifts)
    "COIN",      # Coinbase Global (Crypto exchange high-beta cyclicality)
    "HOOD",      # Robinhood Markets (Retail trading volume cycles)
    "RBLX",      # Roblox (Metaverse/gaming platform user monetization)
    "AFRM",      # Affirm Holdings (Buy-now-pay-later credit risk exposure)
    "UPST",      # Upstart Holdings (AI lending platform macroeconomic sensitivity)
    "DASH",      # DoorDash (Delivery logistics margin expansion phase)

    # ==========================================
    # 3. EMERGING MARKETS: LATIN AMERICA & AFRICA
    # ==========================================
    "BSBR",      # Banco Santander Brasil (Banking)
    "SUZ",       # Suzano (Brazil - Pulp and paper producer)
    "GGB",       # Gerdau (Brazil - Steel manufacturing)
    "CX",        # Cemex (Mexico - Building materials)
    "ASR",       # Grupo Aeroportuario del Sureste (Mexico - Airport operator)
    "PAC",       # Grupo Aeroportuario del Pacífico (Mexico - Airport operator)
    "OMAB",      # Grupo Aeroportuario del Centro Norte (Mexico - Airport operator)
    "VIST",      # Vista Energy (Argentina/Mexico - Oil and gas)
    "GLOB",      # Globant (Argentina origin - IT services)
    "ARCO",      # Arcos Dorados (LatAm - McDonald's franchise operator)
    "CRESY",     # Cresud (Argentina - Agricultural enterprise)
    "MELI",      # MercadoLibre (LatAm e-commerce anchor)
    "NTO.JO",    # Naspers / Prosus proxies / Naspers limited (South Africa consumer tech)
    "SBK.JO",    # Standard Bank Group (South Africa banking)
    "SOL.JO",    # Sasol Ltd (South Africa - Integrated energy and chemicals)

    # ==========================================
    # 4. EMERGING MARKETS: ASIA-PACIFIC & INDIA
    # ==========================================
    "9988.HK",   # Alibaba Group (Hong Kong primary line)
    "0700.HK",   # Tencent Holdings (Hong Kong)
    "3690.HK",   # Meituan (China - Local services and e-commerce)
    "1211.HK",   # BYD Company (China - Electric vehicles and batteries)
    "0981.HK",   # Semiconductor Manufacturing International Corp (SMIC - China)
    "2330.TW",   # Taiwan Semiconductor Manufacturing Co (Taiwan primary line)
    "2454.TW",   # MediaTek (Taiwan - Fabless semiconductor design)
    "2317.TW",   # Hon Hai Precision Industry / Foxconn (Taiwan - Electronics manufacturing)
    "005930.KS", # Samsung Electronics (South Korea - Memory and consumer electronics)
    "000660.KS", # SK Hynix (South Korea - Semiconductor memory)
    "035420.KS", # NAVER Corp (South Korea - Search engine and digital ecosystem)
    "035720.KS", # Kakao Corp (South Korea - Messaging and internet platform)
    "RELIANCE.NS", # Reliance Industries (India - Energy, retail, and telecom)
    "TCS.NS",    # Tata Consultancy Services (India - IT services)
    "HDFCBANK.NS", # HDFC Bank (India - Financial services)
    "INFY.NS",   # Infosys (India primary listing)
    "ICICIBANK.NS", # ICICI Bank (India)
    "BHARTIARTL.NS", # Bharti Airtel (India - Telecommunications)
    "ITC.NS",    # ITC Limited (India - Conglomerate and consumer goods)
    "LT.NS",     # Larsen & Toubro (India - Engineering and construction)

    # ==========================================
    # 5. GLOBAL RESOURCES, MINING & INDUSTRIAL STALWARTS
    # ==========================================
    "BHP",       # BHP Group (Australia/Global - Mining and resources)
    "RIO",       # Rio Tinto (UK/Australia - Metals and mining)
    "VALE",      # Vale SA (Brazil - Iron ore)
    "FCX",       # Freeport-McMoRan (US - Copper and gold mining cyclicality)
    "SCCO",      # Southern Copper Corporation (Peru/Mexico copper mining)
    "TECK",      # Teck Resources (Canada - Diversified mining)
    "PAAS",      # Pan American Silver (Canada - Precious metals)
    "AEM",       # Agnico Eagle Mines (Canada - Gold mining quality compounder)
    "WPM",       # Wheaton Precious Metals (Canada - Streaming royalty model)
    "FNV",       # Franco-Nevada Corporation (Canada - Royalty and streaming)
    "AGI",       # Alamos Gold (Canada)
    "ERO",       # Ero Copper (Canada/Brazil - Copper mining growth)
    "NEM",       # Newmont Corporation (US - Gold mining)
    "AA",        # Alcoa Corporation (US - Aluminum producer cyclicality)
    "CLF",       # Cleveland-Cliffs (US - Iron ore and steel manufacturing)
    "X",         # United States Steel (US - Cyclical steel manufacturing)
    "STLD",      # Steel Dynamics (US - Efficient mini-mill steel producer)
    "NUE",       # Nucor Corporation (US - Steel manufacturer)
    "MLM",       # Martin Marietta Materials (US - Aggregates and construction materials)
    "VMC"        # Vulcan Materials (US - Construction aggregates)
]