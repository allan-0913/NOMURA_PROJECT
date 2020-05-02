def NomuraData():
    HData = open("nomura_global_equity.csv").readlines()
    MData = [line.strip(",\n").split(";") for line in HData]
    for i in range(len(MData)):
        MData[i][1] = float(MData[i][1])
        MData[i][2] = float(MData[i][2])
    return MData