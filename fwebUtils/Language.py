from fwebUtils import LIST, Ext
from fwebUtils.LOGGER import Log
Log = Log("FWEB.Futils.Language")

"""
    -> Tokenizing/Splitting Words from a String.
"""

def to_words_v1(content: str):
    content = replace(content, ".", ",", ";", "\n", "  ")
    s = content.split(" ")
    newS = remove_empty_strings(s)
    return newS

def remove_empty_strings(list_of_strs: []):
    newS = []
    for word in list_of_strs:
        if word == '':
            continue
        newS.append(word)
    return newS

def replace(content, *args):
    for arg in args:
        content = content.replace(arg, " ")
    return content

def score_complete_tokenization(tokenization: dict):
    result = {}
    for key in tokenization.keys():
        token_list = tokenization[key]
        result[key] = score_words(token_list)
    return result

@Ext.safe_args
def complete_tokenization_v2(content, toList=True):
    """ PUBLIC """
    toStr = LIST.to_str(content)
    tokens = to_words_v1(toStr)
    bi_grams = to_x_grams(tokens, 2)
    tri_grams = to_x_grams(tokens, 3)
    quad_grams = to_x_grams(tokens, 4)
    if toList:
        return tokens + bi_grams + tri_grams + quad_grams
    else:
        return {"tokens": tokens, "bi_grams": bi_grams, "tri_grams": tri_grams, "quad_grams": quad_grams}

def to_x_grams(tokens, x):
    """ PUBLIC """
    if type(tokens) == str:
        tokens = to_words_v1(tokens)
    i = 0
    x_grams = []
    if len(tokens) < x:
        Log.d("found none", tokens)
        return x_grams
    for _ in tokens:
        if i+x > len(tokens):
            break
        phrase = ""
        for c in range(x):
            phrase = combine_words(phrase, tokens[i+c])
        x_grams.append(phrase)
        i += 1
    return x_grams

def to_bi_grams_v2(tokens):
    """ PUBLIC HELPER """
    return to_x_grams(tokens, 2)

def to_tri_grams_v2(tokens):
    """ PUBLIC HELPER """
    return to_x_grams(tokens, 3)

def to_quad_grams_v2(tokens):
    """ PUBLIC HELPER """
    return to_x_grams(tokens, 4)


"""
    -> FAIR UTILS
"""

def score_words(words):
    result = {}
    for word in words:
        if word in result.keys():
            tempValue = result[word]
            result[word] = tempValue + 1
        else:
            result[word] = 1
    return result

def combine_words(*words):
    """ Combines two strings together. """
    temp_word = ""
    if len(words) > 0:
        for word in words:
            temp_word += " " + word.strip()
        return temp_word.strip()
    return str(words).strip()

@Ext.safe_args
def combine_args_str(content: str) -> str:
    temp = ""
    for item in content:
        temp += " " + str(item)
        print(temp)
    return str(temp).strip()

# if __name__ == '__main__':
#     test = "testing1"
#     test2 = "testing2"
#     print(combine_args_str([test, test2], "test3"))

def remove_ing(word):
    if word.endswith("ing"):
        return word[:-3]
    elif word.endswith("ings"):
        return word[:-4]
    return False

def remove_apos(word):
    word = word.replace("'", "")
    return word

# if __name__ == '__main__':
#     test = "Reddit Email 0 Shares\n\nMost of the world has decriminalized cannabis, and many nations have implemented regulated cannabis industries. Medical marijuana is often the precursor to personal-use cannabis legislation because it’s easier for cannabis-wary thinkers to consider weed as medicine than recreation.\n\nMedical marijuana advocates are primarily responsible for the growing accessibility of cannabis in certain regions in Africa, North America, South America, Europe, and Australia. However, most Asian countries continue to uphold cannabis prohibition, even for medical use.\n\nContinue Reading Below\n\nKeep reading to discover the legal status of medical marijuana around the world.\n\nAsia\n\nThe cannabis plant’s origins are most likely in Asia. However, the world’s largest continent is home to some of the staunchest cannabis laws. Cannabis was first domesticated in or near China, Pakistan, or Afghanistan and popularized in India. However, getting caught with pot in one of those countries can result in severe fines and penalties:\n\nConvicted cannabis smokers can spend a couple of weeks in jail in China.\n\nPakistan will imprison people for two years for cannabis possession.\n\nIn Afghanistan, you can spend three months in prison.\n\nPossession of small amounts of cannabis can land someone up to six months prison time in India.\n\nHowever, there are signs that the last continent to resist cannabis legalization is shifting paradigms. In 2018, South Korea was the first Asian country to legalize medical marijuana. That same year, Japan approved clinical trials for cannabis-based medicine, Epidiolex. Thailand legalized comprehensive medical marijuana legislation in 2019.\n\nThis January, Thailand also became the first country in Asia to decriminalize marijuana. There is no legislation authorizing a legal cannabis retail industry or clear rules about what happens to people found with cannabis. However, weed is no longer on Thailand’s Narcotics Control Board drug schedule. It’s one step for stoners in Thailand, one giant leap for Asia’s deeply-rooted unregulated cannabis market.\n\nContinue Reading Below\n\nAfrica\n\nBefore cannabis was popular in the Caribbean, South America, or North America, it was cultivated throughout Africa. Cannabis made its way west because of the enslavement and trafficking of African people. Despite a long history with weed, only ten African countries have legalized or decriminalized the medicinal plant.\n\nCannabis is legal for medical use in a handful of African countries, including Uganda, Zimbabwe, Rwanda, Morocco, Lesotho, Zambia, and South Africa.\n\nIn 2018, the South African Constitutional Court also ruled that personal cannabis cultivation was permissible and mandated the government to enact a personal-use law within two years.\n\nContinue Reading Below\n\nDespite strict prohibition across most of the continent, Africa houses a thriving unregulated cannabis industry. According to New Frontier Data’s “Africa Regional Hemp & Cannabis Report,” the average annual cannabis use rate in Africa is 11.4 percent, almost twice as high as the 12 percent global average. In other words, regulated medical marijuana is mostly inaccessible, but unregulated weed is everywhere.\n\nSouth America\n\nBecause of the slave trade’s movement from Europe and Africa to the west, South America acted as a bridge between cannabis (a plant native to eastern regions) and North America. Cannabis traveled from Brazil to Mexico, and when thousands of refugees fled to the United States to avoid the bloody Mexican Revolution, they brought recreational cannabis use with them.\n\nIn 2013, Uruguay became the first country in the world to legalize cannabis. Consumers can purchase cannabis at pharmacies but, as things tend to go with cannabis laws, the process has been muddled with institutional barriers. For example, many banks refuse to work with pharmacies selling weed because of U.S. and international anti-weed laws.\n\nDespite these obstacles, Uruguay illuminated a path toward legality for the rest of the continent (and the world). Though personal use remains generally unlawful, medical marijuana is legal in most South American countries, including Argentina, Chile, Colombia, and Peru.\n\nContinue Reading Below\n\nEurope\n\nCannabis spread throughout Asia, Africa, and Europe because of Aryan nomadic tribes. Today, medical marijuana is legal to a degree in at least 17 European countries, including Poland, Romania, Norway, Germany, Italy, and Greece. However, medical marijuana is limited mainly to the cannabis extract, nabiximol (Sativex).\n\nIn most European countries, it is illegal to grow your own bud, and it’s rare for patients to have the authorization to access flower for medicinal use. Here’s some perspective: just this past October, Luxembourg became the first country in Europe to legalize home grows.\n\nBut what about the Netherlands? While Amsterdam’s “coffee shops” are known for selling cannabis, medical weed laws throughout the Netherlands are not as liberal as you’d think. Medical patients can access medical marijuana at a pharmacy with a doctor’s prescription. But personal cannabis use is illegal. As in the U.S., the national government chooses to deprioritize most cannabis law violations.\n\nNorth America\n\nNorth America is home to two of the most notable models of medical cannabis legalization in the world: the United States and Canada.\n\nContinue Reading Below\n\nUnited States federal laws prohibit cannabis possession and consumption, but most of the country’s states have legalized weed in some form for medical use. Idaho, Wyoming, Kansas, and South Carolina are the only states in the U.S. that have kept all cannabis products (including CBD) illegal (though, at the time of this writing, South Carolina is also currently in talks to start a medical marijuana program.\n\nJust north of a very discombobulated U.S., Canada is the second country in the world to legalize recreational cannabis at the national level. Medical marijuana was legalized in Canada in 2014, and the nation’s medical industry made it possible for Canadians to quickly adapt to the personal-use market created by national legalization in 2018.\n\nContinue Reading Below\n\nAustralia\n\nAustralia legalized medical marijuana in 2016. On paper, Australia’s medical marijuana program is comprehensive and progressive, authorizing patients to access several forms of high and low-THC cannabis, including oils, capsules, and flower with a prescription. However, the reality is far less idyllic. As one 2019 documentary series revealed, bureaucratic inefficiencies block access and force patients to rely on the unregulated market to get the quick relief they need.\n\nEven in nations where cannabis legalization is patchy or missing altogether, the demand for medical marijuana is on the rise. As research continues to expose cannabis’ therapeutic utility, legislation worldwide is likely to reflect patients’ needs.\n\nMedical Marijuana Around the World was last modified: by"
#     tokenization = complete_tokenization_v2(test, toList=False)
#     scores = score_complete_tokenization(tokenization)
#     print(scores)