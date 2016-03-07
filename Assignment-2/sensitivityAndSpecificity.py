
tp = 238.0
tn = 236.0
fp = 4.0
fn = 2.0

precision = tp / (tp+fp)
recall = tp / (tp+fn)
fmeasure = 2 * ((precision * recall) / (precision + recall))

print "Precision: " + str(precision)
print "Recall   : " + str(recall)
print "Fmeasure : " + str(fmeasure)