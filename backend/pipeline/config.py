# Configuration for Phase 1: Data Pipeline
# Stores target URLs and ingestion settings.

# Additional metadata configuration
DATA_SOURCE_CONFIG = {
    "amc": "HDFC Mutual Fund",
    "data_origin": "Official Scheme Pages & Regulatory Guidance"
}

# The target URLs for verified factual retrieval
TARGET_URLS = [
    # HDFC Scheme Pages (Groww)
    "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth",
    "https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth",
    "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/hdfc-liquid-fund-direct-growth",
    "https://groww.in/mutual-funds/hdfc-multi-cap-fund-direct-growth",
    
    # Official HDFC AMC Services & FAQ Pages
    "https://www.hdfcfund.com/services/faqs",
    "https://www.hdfcfund.com/services/faqs/smart-account-statement",
    "https://www.hdfcfund.com/services/faqs/central-know-your-customer-ckyc-new",
    "https://www.hdfcfund.com/services/faqs/faqs-fatca-crs",
    
    # AMFI Investor Education & Guidance
    "https://www.amfiindia.com/investor",
    "https://www.amfiindia.com/investor/knowledge-center-info?zoneName=NetAssetValueNAV",
    "https://www.amfiindia.com/investor/become-mf-distributor?zoneName=sip",
    "https://www.amfiindia.com/investor/become-mf-distributor?zoneName=KnowYourCustomer"
]
