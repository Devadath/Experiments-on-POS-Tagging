
#!/usr/bin/python
import sys
 
class Root:
    '''
    Creates the root node for Trie 
    '''
    def __init__(self):
        self.root = {}  # Main root directory class, where you can find the unique list ofthe first character of every word will be stored
 
 
class CharTrie:
    '''
    Trie implementation
    '''
    def __init__(self):
        self.list = []
        self.prob ={}
        self.count = {}
        self.address ={}
        self.children = {}
        self.char = 'c'
        self.i = 1
        self.j = 0
        self.h = 0
    def addWord (self, w_list, tag, Index=1):
        w_count = self.count.get(tag)
        if w_count == None:
            self.count.setdefault(tag,1)
        else:
            self.count[tag]+= 1
        #print (self.count,"count")
 
        if Index < len(w_list):
            nextnode  = self.children.get(w_list[Index])
            if nextnode == None:
                nextnode = CharTrie()
                nextnode.char = w_list[Index]
                self.children.setdefault(w_list[Index],nextnode)
                #print ("CHARCTER ADDED", w_list[Index])
                self.children[w_list[Index]].addWord(w_list, tag, Index+1)
 
            else:
                self.children[w_list[Index]].addWord(w_list, tag, Index+1)
    def prob_class(self, w_list,prob_dict, Index=0):
        res = self.get_total_freq(self.count,prob_dict)
        Index+=1
        if Index < len(w_list):
            nextnode  = self.children.get(w_list[Index])
            if nextnode != None:
                nextnode.prob_class(w_list,prob_dict,Index)
        return res
    def get_total_freq(self,dict,prob_dict):
        for i in dict:
            f_l = dict.values()
            prob = float(dict[i])/sum(f_l)
            node_count = prob_dict.get(i)
            #print (prob_dict,node_count,"nd")
            if node_count == None:
                prob_dict[i] = prob
            else:
                #print ("yes")
                #print (node_count, prob, node_count+prob)
                k = node_count+prob
                prob_dict[i] = k
        return prob_dict
if (__name__ == "__main__"):
 
    Data = open(sys.argv[1],"r", encoding = "UTF-8")
    input_Data = sys.argv[2]
    l = list(input_Data)
    m = l
    print (input_Data)
    Data_text = Data.readlines()
    HeadNode = Root()
    for line in Data_text:
        line = line.strip()
        line = line.split("\t")
        if len(line) < 2:
            continue
        Word = line[0]
        Tag = line[1]
 
        if Word[0] not in HeadNode.root:
            k = list(Word)
            HeadNode.root[Word[0]] = CharTrie()
            HeadNode.root[Word[0]].char=Word[0]
            #print ("CHARCTER ADDED",HeadNode.root[Word[0]].char)
            HeadNode.root[Word[0]].addWord(k,Tag,1)
        else:
            k = list(Word)
            HeadNode.root[Word[0]].addWord(k,Tag,1)
    #print (HeadNode.root , "HeadNode")
    ReverseNode = Root()
    #print(ReverseNode, "ReverseNode")
    #print(Data_text)
    for line in Data_text:
        #print (line,"line")
        line = line.strip()
        line = line.split("\t")
        if len(line) < 2:
            continue
        Word = line[0]
        listed = list(Word)
        word = "".join([i for i in listed[::-1]])
        #print (word,"word")
        Tag = line[1] 
        if word[0] not in ReverseNode.root:
            k = list(word)
            ReverseNode.root[word[0]] = CharTrie()
            ReverseNode.root[word[0]].char=word[0]
        #   print ("CHARCTER ADDED",ReverseNode.root[word[0]].char)
            ReverseNode.root[word[0]].addWord(k,Tag,1)
        else:
            k = list(word)
            ReverseNode.root[word[0]].addWord(k,Tag,1)
    print (ReverseNode.root)
    def normaliser(dict,norm_dict):
        for i in dict:
            f_l = dict.values()
            prob = float(dict[i])/sum(f_l)
            node_count = norm_dict.get(i)
            if node_count == None:
                norm_dict[i] = prob
            else:
                k = node_count+prob
                norm_dict[i] = k
        return norm_dict
    if m[0] in HeadNode.root :
        k = HeadNode.root[m[0]].prob_class(m,{},0)
        normalised_prefix= normaliser(k,{})
    l.reverse()
    if l[0] in ReverseNode.root:
        k = ReverseNode.root[l[0]].prob_class(l,{},0)
        normalised_suffix = normaliser(k,{})
 
    print (normalised_prefix,normalised_suffix)
    probability = lambda k,l : {(key,k.get(key,1)*l.get(key,1)) for key in set(list(k.keys())+list(l.keys()))}
    final_prob = probability(normalised_prefix,normalised_suffix)
 
    print (final_prob,"final")
