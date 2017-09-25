import trees
import treePlotter as tp

fr = open('lenses.txt')
lenses = [inst.strip().split('\t') for inst in fr.readline()]
lensesLabels=['age', 'prescript', 'astigmatic', 'tearRate']
lensesTree = trees.createTree(lenses, lensesLabels)
print type(lensesTree)
tp.createPlot(lensesTree)