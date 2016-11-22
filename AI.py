"""AI class for Mao card game"""
import sklearn.tree as sk
import sklearn.preprocessing as pre
import numpy as np
import pydotplus

class AI:
    """AI superclass for hands and card selection of all AIs"""
    def __init__(self, h):
        self.hand = h

    def card_select(self, topcard):
        """Play an appropriate card, if there is one"""
        print(topcard)
        print(self.hand)
        validturn = True
        for card in self.hand.cards:
            if card.rank == topcard.rank or card.suit == topcard.suit:
                self.hand.rem_card(card)
                print("Card played is {}".format(card))
                topcard = card
                break
        else:
            validturn = False
        return topcard, validturn

class AIperf(AI):
    """AI that already knows the rules of Mao"""
    def __init__(self, h, rankr, suitr):
        super(AIperf, self).__init__(h)
        self.hand = h
        self.r = rankr
        self.s = suitr

    def turn(self, topcard, f, l):
        """Perform a turn, playing an appropriate card and following all rules"""
        card, validturn = self.card_select(topcard)
        actions = []
        if validturn:
            r = card.rank
            s = card.suit
            for i in list(self.r.keys()):
                if r == i:
                    actions += [self.r[i]]
            for i in list(self.s.keys()):
                if s == i:
                    actions += [self.s[i]]
        print("The actions are: ", actions)
        return card, actions

    def drawtree(self):
        """Does nothing actually. Sorry."""
        return "tree"

class AIplay(AI):
    """AI that learns to play Mao from previous correct moves"""
    def __init__(self, h):
        """Initialize AI with a hand."""
        super(AIplay, self).__init__(h)
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

    def drawtree(self):
        print("Trying to draw a tree")
        dot_data = sk.export_graphviz(self.clf, out_file=None,
                            class_names=self.le.classes_,
                            filled=True, rounded=True,
                            special_characters=True)
        print("Tree?")
        graph = pydotplus.graph_from_dot_data(dot_data)
        print("Tree!")
        graph.write_pdf("mao.pdf") 
        print("Trees.... They, are, usssss.....")

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
        """Choose an appropriate card and predict actions"""
        actions = []
        topcard, validturn = self.card_select(topcard)
        X = [topcard.suit, topcard.rank]
        if not validturn:
            return topcard, actions
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
