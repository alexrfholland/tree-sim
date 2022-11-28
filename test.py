import pandas as pd
import setting as settings

test = {'hello' : [1,2,3,4], 'bellow' : [1,2,3,4]}

filePath = f'{settings.SUSTAINABILITY}CSV/cumulative resources - {settings.scenario}.csv'
dfTotals = pd.DataFrame(test)
print(dfTotals)
dfTotals.to_csv(filePath)
1

