from collections import OrderedDict
import sys

def islist(obj):
    if ("list" in str(type(obj))):
        return True
    else:
        return False

class CKY_parser:
    def __init__(self, cnf_path):
        self.rules = {}
        self.load_rules(cnf_path)

        if input("Show display trees? (y/n)") == "y":
            self.show_display_tree = True
        else:
            self.show_display_tree = False


    def load_rules(self, path):
        f = open(path, "r")
        for line in f:
            temp = line.split("-->")
            result = temp[0].split(" ")[0]
            symbols = temp[1][1:-1].split(" ")
            if len(symbols) == 1:
                if symbols[0] not in self.rules:
                    self.rules[symbols[0]] = [result]
                else:
                    self.rules[symbols[0]].append(result)
            else:
                if symbols[0] not in self.rules:
                    self.rules[symbols[0]] = {
                        symbols[1]: [result]
                    }
                else:
                    if symbols[1] not in self.rules[symbols[0]]:
                        self.rules[symbols[0]][symbols[1]] = [result]
                    else:
                        self.rules[symbols[0]][symbols[1]].append(result)



    '''
    Structure of the parse table:
        [{s: [[index1, index2],[index1, index2]]}, {}, {}, {}]
        [[] [] [] []]
    '''

    def create_parse_table(self, sentence):
        num_words = len(sentence.split(" "))
        words = sentence.split(" ")
        for word in words:
            if word not in self.rules:
                return False
        self.parse_table = [[{} for x in range(num_words+1)] for y in range(num_words+ 1)]

        for j in range(num_words+1):
            i_indices = [x for x in range(j)]

            i_indices.reverse()
            for i in i_indices:

                if i== j-1:
                    for non_terminal in self.rules[words[j-1]]:
                        self.parse_table[i][j][non_terminal] = {"terminal": words[j-1]}
                for k in range(i+1, j):
                    self.find_valid_combos(self.parse_table[i][k].keys(), self.parse_table[k][j].keys(), i, j, k)

        return True

    def find_valid_combos(self, list1, list2,i ,j, k):
        for non_terminal1 in list1:
            for non_terminal2 in list2:
                if non_terminal1 in self.rules and non_terminal2 in self.rules[non_terminal1]:
                    for result in self.rules[non_terminal1][non_terminal2]:
                        if result in self.parse_table[i][j]:
                            self.parse_table[i][j][result].append(
                                {
                                    "row-child": non_terminal1,
                                    "col-child": non_terminal2,
                                    "row-child-coords": [i, k],
                                    "col-child-coords": [k, j]
                                }
                            )
                        else:
                            self.parse_table[i][j][result] = [
                                {
                                    "row-child": non_terminal1,
                                    "col-child": non_terminal2,
                                    "row-child-coords": [i, k],
                                    "col-child-coords": [k, j]
                                }
                            ]

    def output_parses(self, num_words):
        if "S" in self.parse_table[0][num_words]:
            valid_parses = self.explore_tree([0,num_words], "S")
            print("VALID SENTENCE\n")
            for i,valid_parse in enumerate(valid_parses):
                print("Valid parse #" + str(i+1) + ":")
                print(self.print_sentence_parse(valid_parse)[1:])
                if self.show_display_tree:
                    self.print_phrase_tree(valid_parse,"")
            print("\nNumber of valid parses: " + str(len(valid_parses)))
        else:
            print("NO VALID PARSES")
    def print_sentence_parse(self, sentence_tree):
        tmp =""
        for key, value in sentence_tree.items():
            if type(value) == str:
                tmp += " [" +key + " " + value + "]"
            else:
                tmp += " [" + key + self.print_sentence_parse(value) + "]"
        return tmp


    def print_phrase_tree(self, phrase, indent):
        for key, value in phrase.items():
            if type(value) == str:
                print(indent + "[" +key + " " + value + "]")
            else:
                print(indent + "[" + key)
                self.print_phrase_tree(value, indent + "   ")
                print(indent + "]")


    def explore_tree(self, coords, parent):

        if "terminal" in self.parse_table[coords[0]][coords[1]][parent]:
            return [
                OrderedDict({
                parent: self.parse_table[coords[0]][coords[1]][parent]["terminal"]
            })
            ]
        else:
            result =[]
            for child_pair in self.parse_table[coords[0]][coords[1]][parent]:
                row_child = self.explore_tree(child_pair["row-child-coords"], child_pair["row-child"])
                col_child = self.explore_tree(child_pair["col-child-coords"], child_pair["col-child"])


                for valid_row_child in row_child:
                    for valid_col_child in col_child:
                        temp_dict = OrderedDict()
                        temp_dict[child_pair["row-child"]] = valid_row_child[child_pair["row-child"]]
                        temp_dict[child_pair["col-child"]] = valid_col_child[child_pair["col-child"]]

                        result.append(
                            OrderedDict({parent: temp_dict})
                        )

            return result



if __name__ == "__main__":


    print("Loading grammar...")
    if len(sys.argv) >= 2:
        cky_parser = CKY_parser(sys.argv[1])
        sentence = input("Enter a sentence: ")
        while (sentence != "quit"):

            if(cky_parser.create_parse_table(sentence)):
                cky_parser.output_parses(len(sentence.split(" ")))
            else:
                print("NO VALID PARSES: Word not in grammar found")
            sentence = input("Enter a sentence: ")
    else:
        print("Please link a path to a grammar file")



