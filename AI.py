"""AI class for Mao card game"""
import sklearn.tree as sk
import sklearn.preprocessing as pre
import numpy as np

class AIplay:
    """AI that learns to play Mao from previous correct moves"""
    def __init__(self, h):
        """Initialize AI with a hand."""
        self.hand = h
        self.clf = sk.DecisionTreeClassifier()
        self.le = pre.MultiLabelBinarizer()
        self.enc = pre.OneHotEncoder(n_values=[4, 13]) #there are 4 suits and 13 ranks
        #whoa that sure is one hot encoder
        self.featrankdict = {}
        self.featsuitdict = {}

    def prep(self, pref, prelab):
        """Preprocess data to pass to learning algorithms."""
        prefeat = pref[:]
        for feat in range(len(prefeat)):
            prefeat[feat] = prefeat[feat][:]
            for f in range(0, 2, 2):
                self.featsuitdict.setdefault(prefeat[feat][f], len(self.featsuitdict))
                self.featrankdict.setdefault(prefeat[feat][f+1], len(self.featrankdict))
                prefeat[feat][f] = self.featsuitdict[prefeat[feat][f]]
                prefeat[feat][f+1] = self.featrankdict[prefeat[feat][f+1]]
        X = self.enc.fit_transform(prefeat).toarray()
        Y = self.le.fit_transform(prelab)
        return X, Y

    def update(self, feat, lab):
        """Fit AI to current data."""
        (feat, lab) = self.prep(feat, lab)
        self.clf.fit(feat, lab)

    def predict(self, X, feat, lab):
        """Predict what actions to take based on X.

        X is [topcard.suit, topcard.rank, top.suit, top.rank]
        feat and lab are unprocessed info about previous moves"""
        self.update(feat, lab)
        for f in range(0, 2, 2): #replace feature strings with numbers
            self.featsuitdict.setdefault(X[f], len(self.featsuitdict))
            self.featrankdict.setdefault(X[f+1], len(self.featrankdict))
            X[f] = self.featsuitdict[X[f]]
            X[f+1] = self.featrankdict[X[f+1]]
        X = np.array(X).reshape(1, -1)
        X = self.enc.transform(X).toarray()
        Y = self.clf.predict(X)
        for y in Y:
            if np.count_nonzero(y) > 0:
                break
        else:
            return []
        if Y.ndim == 1:
            Y = np.array([Y])
        [words] = self.le.inverse_transform(np.array(Y))
        #get predicted labels and transform them into tuple of action strings
        return list(words) #wrap tuple as a list. im sorry this is, many gross conversions

    def turn(self, topcard, f, l):
        """Choose an appropriate card and predicts actions"""
        validturn = True
        print(topcard)
        print(self.hand)
        actions = []
        for card in self.hand.cards:
            if card.rank == topcard.rank or card.suit == topcard.suit:
                self.hand.rem_card(card)
                X = [card.suit, card.rank]
                print("Card played is {}".format(card))
                topcard = card
                break
        else:
            validturn = False
        for y in l:
            if y != []:
                break
        else:
            return topcard, []
        if validturn and f != []:
            print("The previous features are", f)
            print("The previous labels are", l)
            actions = self.predict(X, f, l)
            print("Predicted actions are {}".format(actions))
        return topcard, actions
