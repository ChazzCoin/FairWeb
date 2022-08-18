from F import LIST

urls = [
    "https://towardsdatascience.com/how-to-use-qgis-spatial-algorithms-with-python-scripts-4bf980e39898",
"https://www.cnn.com/2022/03/27/politics/joe-biden-vladimir-putin-ukraine-war/index.html",
"https://towardsdatascience.com/a-step-by-step-guide-to-scheduling-tasks-for-your-data-science-project-d7df4531fc41",
    "https://www.forbes.com/sites/investor/2022/01/28/ethereum-cardano-polygon-solana-avalanche-and-polkadot-deathmatch-who-wins-who-dies/?sh=4292a4897c9b",
"https://finance.yahoo.com/news/metaverse-real-estate-market-growing-115600231.html",
"https://cointelegraph.com/news/price-analysis-1-28-btc-eth-bnb-ada-sol-xrp-luna-doge-dot-avax",
"https://www.forbes.com/sites/investor/2022/01/28/ethereum-cardano-polygon-solana-avalanche-and-polkadot-deathmatch-who-wins-who-dies/?sh=4292a4897c9b",
"https://www.businessinsider.com/tomi-lahren-spoke-at-police-training-event-dismissed-reform-wapo-2022-1",
"https://www.foxbusiness.com/business-leaders/elon-musk-offers-support-to-canadian-truckers-amid-covid-vaccine-mandate",
"https://towardsdatascience.com/a-step-by-step-guide-to-scheduling-tasks-for-your-data-science-project-d7df4531fc41",
"https://www.americanbanker.com/payments/news/inside-ripples-plans-for-mainstream-crypto-payments",
"https://finance.yahoo.com/news/metaverse-real-estate-market-growing-115600231.html",
"https://cointelegraph.com/news/blockchain-metaverse-ecosystems-gain-traction-as-brands-create-digital-experiences",
"https://www.theguardian.com/world/2022/jan/26/biden-threatens-putin-with-personal-sanctions-if-russia-invades-ukraine",
"https://www.americanbanker.com/payments/news/inside-ripples-plans-for-mainstream-crypto-payments",
"https://towardsdatascience.com/decorators-in-python-fundamentals-for-data-scientists-eada7f4eba85",
"https://www.wsj.com/articles/meta-platforms-facebook-fb-q1-earnings-report-2022-1165102219",
"https://www.wsj.com/articles/primary-elections-2022-south-carolina-nevada-races-test-trumps-sway-in-gop-11655199002",
"https://finance.yahoo.com/news/metaverse-real-estate-market-growing-115600231.html",
"https://www.newsobserver.com/news/business/article260136540.html",
"https://www.reuters.com/business/media-telecom/jury-alex-jones-defamation-case-begin-deliberations-punitive-damages-2022-08-05/"

]

import HttpRequest

test1OnlySuccess = []
test2OnlySuccess = []
bothSuccess = []
bothFailed = []

def loop_urls():
    for url in urls:
        test1 = HttpRequest.get_request_v2(url)
        test1Result = LIST.get(0, test1, default=False)
        test2 = HttpRequest.get_request_urllib(url)
        test2Result = LIST.get(0, test2, default=False)
        if test1Result and test2Result:
            bothSuccess.append(url)
        elif test1Result:
            test1OnlySuccess.append(url)
        elif test2Result:
            test2OnlySuccess.append(url)
        else:
            bothFailed.append(url)


loop_urls()
print(test1OnlySuccess)