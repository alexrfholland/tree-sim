JSONOUT = '/Users/alexholland/OneDrive - The University of Melbourne/Stanislav/00 PhD/_Thesis/1 - Ethics/simulation/outputs/'
DEBUG = False


RESOURCES = ["dead","lateral","total","low","medium","high"]
TIMEPERIOD = 240
INTERVAL = 30
DENSITYLOW = 4.65
DENSITYHIGH = 4.65
AREA = 440
INITIALTREES = 50
INITIALDBHMIN = 90
INITIALDBHMAX = 130
INITAGEMIN = 200
INITAGEMAX = 400


MODELRECRUIT = True
MODELDEATH = True

BOUNDS = [0,1000]

RESOURCECAPS = {'total' : 1500, 'lateral' : 800, 'dead' : 350, 'high': 20, 'medium' : 130, 'low' : 1500}
FOCUSRESOURCE = 'high'


TREESTARTDBH = 30
MAXDBH = 145
TREELIFESPAN = [400,600]

# slope of age vs diameter is 1.97 - 2.71 - Gibbons (2009)
TREEGROWRATE = [197, 271]


# mortality rate of 0.006 to 0.024 per year - Gibbons (2009)
DEATHLOW = .006
DEATHHIGH = .024


#recruitment stats from Gibbons (2009)
RECRUITMULTIPLIER = 2

##artificial
ARTNUMBER = 20
ARTINTERVAL = 3
ARTPERFMIN = 0.01
ARTPERFMAX = 0.3
ARTIMPROVE = 0.01

ARTLIFE = 5

UPDATEMESSAGE = '######### \t ######### \t ########'


CONSTRICTORDBHLOW = 75
RESOURCEBELOW = 0.5

#folderPath 
FOLDERPATH= "/Users/alexholland/OneDrive - The University of Melbourne/Stanislav/00 PhD/_Thesis/1 - Ethics/simulation/data/resources/"
#filesDict 
FILESDICT = {"dead":"dead-branch-loess", "lateral":"lateral-branch-loess", "total":"total-branch-loess", "low":"low-branch-loess", "medium":"medium-branch-loess", "high":"high-branch-loess"}
#resourceGraph 
RESOURCEGRAPH = ["dead","lateral","total","low","medium","high"]