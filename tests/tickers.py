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
]