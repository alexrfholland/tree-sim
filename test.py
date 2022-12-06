import setting as settings

outputFilePath = settings.MakeFolderPath(settings.SUSTAINABILITY, f'model-outputs/{settings.scenario}-')

for i in range(0,10):
    path = f'{outputFilePath}{i}.csv'
    print(path)
    