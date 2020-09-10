import networkx as nx

# BOND GRAPHS



class system(object):
    def __init__(self, bondlist=[]):
        self.bonds = bondlist # list of bonds
        self.elem_nbrs = self.build_elem_nbrs() # dict(e: nbrlist)
        self.G = nx.Graph(self.elem_nbrs) # graph of bonds to elems

    def add_bond(self, bond):
        self.bonds.append(bond)
        self.elem_nbrs = self.build_elem_nbrs()
        self.G = nx.Graph(self.elem_nbrs)

    def build_elem_nbrs(self):
        bdict = {}
        """ build bond dictionary with
            key = element
            value = neighbors
        """
        for bond in self.bonds:
            nls = bond.nls
            nrs = bond.nrs
            if nls in bdict:
                bdict[nls].append(nrs)
            else:
                bdict.setdefault(nls,[])
                bdict[nls].append(nrs)

            if nrs in bdict:
                bdict[nrs].append(nls)
            else:
                bdict.setdefault(nrs,[])
                bdict[nrs].append(nls)
        return bdict


    def elem_gives(self,elem):
        for nbr in self.elem_nbrs[elem]:
            bond_num = self.get_bond_num(elem,nbr)


    def get_nbrs(self,elem):
        return self.elem_nbrs[elem]

    def get_bond(self,e1,e2):
        for bond in self.bonds:
            if bond.nrs == e1 and bond.nls == e2:
                return bond
            elif bond.nrs == e2 and bond.nls == e1:
                return bond
        return None

    def get_bond_num(self,e1,e2):
        for bond in self.bonds:
            if bond.nrs == e1 and bond.nls == e2:
                return bond.num
            elif bond.nrs == e2 and bond.nls == e1:
                return bond.num
        return -1

    def get_single_ports(self):
        sp = []
        for p in list(self.G.nodes):
            num_friends = len(self.elem_nbrs[p])
            if num_friends == 1:
                sp.append(p)
        return sp

    def __repr__(self):
        rstring  = "system(["
        for bond in self.bonds:
            bstring = f'bond({bond.num},"{bond.nls}","{bond.nrs}","{bond.csd}", "{bond.ped}"),\n'
            rstring += bstring
        rstring += '])'
        return rstring


class SE(object):
    def __init__(self, name=None, bond):
        self.name = name
        self.etype = 'SE'
        self.bond = bond

    def __str__(self):
        return f'{self.etype}:{self.name:5s}, {bond}'


class element(object):
    def __init__(self, name=None):
        self.name = name
        self.etype = self.get_type_from_name()
        self.ports = []


    def __str__(self):
        return f'{self.etype}:{self.name:5s}'

    def get_type_from_name(self):
        if self.name.startswith('SE'):
            return 'SE'
        elif self.name.startswith('SF'):
            return 'SF'
        elif self.name.startswith('R'):
            return 'R'
        elif self.name.startswith('C'):
            return 'C'
        elif self.name.startswith('0J'):
            return '0J'
        elif self.name.startswith('1J'):
            return '1J'
        elif self.name.startswith('TF'):
            return 'TF'
        else:
            return None

    def get_value(self):
        if self.gives == 'e':
            self.value = 'e'
            return self.value
        else:
            self.value = 'f'
            return self.value



class bond(object):
    def __init__(self, number, node_left, node_right, stroke_dir, pos_e_dir):
        self.nls = node_left
        self.nrs = node_right
        self.num = number
        if isinstance(stroke_dir, direction):
            self.csd = stroke_dir.get_dir()
        else:
            self.csd = get_dir_from_str(stroke_dir)
        if isinstance(pos_e_dir, direction):
            self.ped = pos_e_dir.get_dir()
        else:
            self.ped = get_dir_from_str(pos_e_dir)

    def __str__(self):
        CSL = '|'
        CSR = '|'
        PEL = '<'
        PER = '>'
        if self.csd == 'R':
            CSL = ' '
        else:
            CSR = ' '
        if self.ped == 'R':
            PEL = ' '
        else:
            PER = ' '
        return f'[{self.nls:5s}] {CSL}{PEL}__{self.num:2d}__{PER}{CSR} [{self.nrs:5s}]'

    def __repr__(self):
        return f'bond({self.num},"{self.nls}","{self.nrs}", "{self.csd}", "{self.ped}")'

    @classmethod
    def from_bond_string(cls, bs):
        csl = bs[8]
        pel = bs[9]
        if csl == '|':
          cs_dir = 'L'
        else:
          cs_dir = 'R'

        if pel == '<':
          pe_dir = 'L'
        else:
          pe_dir = 'R'

        num = int(bs.split('__')[1])
        NL = bs[1:6].strip()
        NR = bs[-6:-1].strip()
        #print(f'im going to call with: bond({num}, {NL}, {NR}, {cs_dir}, {pe_dir})')
        return cls( num , NL, NR, cs_dir, pe_dir)




class direction:
    def __init__(self, pos):
        self.pos = get_dir_from_str(pos)

    def __call__(self, pos):
        return get_dir_from_str(pos)

    def __repr__(self):
        return f'direction(\"{self.pos}\")'

    def __str__(self):
        return f'{self.pos}'

    def get_dir(self):
        return f'{self.pos}'

def get_dir_from_str(instr):
    tmpstr = instr.lower()
    #print(f'instr = {instr}, now tmpstr = {tmpstr}')
    if tmpstr == 'r':
        #print('tmpstr is equal to r, returning R')
        return f'R'
    elif tmpstr == 'right':
        #print('tmpstr is equal to right, returning R')
        return f'R'
    else:
        #print('tmpstr else, returning L')
        return f'L'

