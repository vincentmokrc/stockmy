class AnnouncementCategory(object):
    AdditionalListing = {'Symbol' : 'AL', 'Index' : 1}
    AnnualAuditedAccount = {'Symbol' : 'AA' , 'Index' : 2}
    AnnualReport = {'Symbol' : 'AR' , 'Index' : 3}
    ChangeCorporateInformation = {'Symbol' : 'CI'+'%2'+'CCOCI' ,'Index' : 4}
    ChangeShareholdings = {'Symbol' : 'SH' , 'Index' : 5}
    ShareholdersNotice = {'Symbol' : 'CS' , 'Index' : 6}
    SecuritiesDelisting = {'Symbol' : 'DLCO' , 'Index' : 7}
    Entitlements = {'Symbol' : 'EA'+'%2'+'CENCO' , 'Index' : 8}
    ExpiryMaturityTermination = {'Symbol' : 'ES' , 'Index' : 9}
    FinancialResults = {'Symbol' : 'FA' , 'Index' : 10}
    GeneralAnnouncement = {'Symbol' : 'GA' , 'Index' : 11}
    GeneralMeetings = {'Symbol' : 'GM'+'%2'+'CMECO' , 'Index' : 12}
    IPOAnnouncement = {'Symbol' : 'IO' , 'Index' : 13}
    ImportantRevelevantDates = {'Symbol' : 'TR', 'Index' : 14}
    InvestorAlert = {'Symbol' : 'IA' , 'Index' : 15}
    ListingCirculars = {'Symbol' : 'LC' , 'Index' : 16}
    ListingInformationProfile = {'Symbol' : 'IP' , 'Index' : 17}
    Prospectus = {'Symbol' : 'PP' , 'Index' : 18}
    ReplyToQuery = {'Symbol' : 'RQ' , 'Index' : 19}
    SharesBuyBack = {'Symbol' : 'SB' , 'Index' : 20}
    SpecialAnnouncements = {'Symbol' : 'SA' , 'Index' : 21}
    TakeoverOffer = {'Symbol' : 'TECO' , 'Index' : 22}
    TransferListing = {'Symbol' : 'TL'+'%2'+'CTRFL' , 'Index' : 23}
    UnusualMarketActivity = {'Symbol' : 'UMA', 'Index' : 24}

class Market(object): 
    MainMarket = {'Symbol' : 'MAIN-MARKET' , 'Index' : 1}
    AceMarket = {'Symbol' : 'ACE-MKT' , 'Index' : 2}
    LeapMarket = {'Symbol' : 'LEAP-MKT' , 'Index' : 3}
    Warrants = {'Symbol' : 'WARRANTS' , 'Index' : 4}
    ETF = {'Symbol' : 'ETF' , 'Index' : 5}
    Bond = {'Symbol' : 'BOND'+'%26'+'LOAN' , 'Index' : 6}

class MarketType(object):
    main_market = {'Symbol' : 'main_market' , 'Index' : 1}
    ace_market = {'Symbol' : 'ace_market' , 'Index' : 2}
    leap_market = {'Symbol' : 'leap_market' , 'Index' : 3}
    lfx_market = {'Symbol' : 'lfx_market' , 'Index' : 4}
    pn17_and_gn13_companies = {'Symbol' : 'pn17_and_gn13_companies' , 'Index' : 5}

class DateString(object):
    
    def __init__(self,day,month,year):
        self.day = day
        self.month = month
        self.year = year

    def get_format_date(self):
        return "{:02d}".format(self.day) +"%2F"+ "{:02d}".format(self.month) +"%2F"+ ("%s"%(self.year)) 