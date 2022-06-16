import settings.setting as settings



SCENARIOS = ['intact','existing','replanting','prosthetics']

def UpdateForScenarios():
    #INTACT
    #death  figures from 'our proposal' in Table 1 of Gibbons et al., “The Future of Scattered Trees in Agricultural Landscapes.”
    
    """settings.scenario = "Intact"
    settings.modelRecruit = True
    settings.modelProsthetics = False
    settings.existingTrees = True
    settings.deathHigh = 0.010
    settings.deathLow = 0.003

    #30: 2032, 44: 1668, 56: 1389, 70: 1120, 83: 917, 96: 773, 109: 642, 121: 526

    #EXISTING
    settings.scenario = "Business-As-Usual"
    settings.modelRecruit = False
    settings.modelProsthetics = False
    settings.existingTrees = False
    settings.deathHigh = 0.035


    #REPLANTING
    settings.scenario = "Continuous Replanting"
    settings.modelRecruit = True
    settings.modelProsthetics = False
    settings.existingTrees = False"""

    #PROSTHETICS
    settings.scenario = "Replanting and Prosthetics"
    settings.modelRecruit = True
    settings.modelProsthetics = True
    settings.existingTrees = False

    print (f'death changed to {settings.deathHigh}')






