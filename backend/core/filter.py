



class Filter:
    def equals(self, x_list, column, y):
        filtered = []
        for x in x_list:
            if(getattr(x, column)==str(y)):
                filtered.append(x)
        return filtered
    
    def biggerThan(self, x_list, column, y):
        filtered = []
        for x in x_list:
            if(int(getattr(x, column))>int(y)):
                filtered.append(x)
        return filtered
    
    
    def lessThan(self, x_list, column, y):
        filtered = []
        for x in x_list:
            if(int(getattr(x, column))<int(y)):
                filtered.append(x)
        return filtered