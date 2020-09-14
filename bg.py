import networkx as nx

# BOND GRAPHS

class bond(object):
    def __init__(self, number, node_left, node_right, stroke_dir, pos_e_dir):
        self.nls = node_left
        self.nrs = node_right
        self.num = number
        self.e = 'e' + "_" + str(self.num)
        self.f = 'f' + "_" + str(self.num)
        if isinstance(stroke_dir, direction):
            self.csd = stroke_dir.get_dir()
        else:
            self.csd = get_dir_from_str(stroke_dir)
        if isinstance(pos_e_dir, direction):
            self.ped = pos_e_dir.get_dir()
        else:
            self.ped = get_dir_from_str(pos_e_dir)

    def set_e(self, e):
        self.e = e + "_" + str(self.num)

    def set_f(self, f):
        self.f = f + "_" + str(self.num)

    def print_rev(self):
        CSL = '|'
        CSR = '|'
        PEL = '>'
        PER = '<'
        if self.csd == 'R':
            CSL = ' '
        else:
            CSR = ' '
        if self.ped == 'R':
            PEL = ' '
        else:
            PER = ' '
        return f'[{self.nrs:5s}] {CSR}{PER}__{self.num:2d}__{PEL}{CSL} [{self.nls:5s}]'

    def is_ped_into_elem(self,elem_name):
        if self.nls == elem_name and self.ped == 'L':
            return True
        elif self.nrs == elem_name and self.ped == 'R':
            return True
        else:
            return False

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

    def get_elem_bonds(self, elem):
        bonds = []
        nbrs = self.elem_nbrs[elem]
        for nbr in nbrs:
            b = self.get_bond(elem, nbr)
            bonds.append(b)
        return bonds

    def get_nbrs(self,elem):
        return self.elem_nbrs[elem]

    def get_bond(self,e1,e2):
        for bond in self.bonds:
            if bond.nrs == e1 and bond.nls == e2:
                return bond
            elif bond.nrs == e2 and bond.nls == e1:
                return bond
        return None

    def get_bond_bynum(self,num):
        for bond in self.bonds:
            if bond.num == num:
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

    def get_two_ports(self):
        elist = []
        for p in list(self.G.nodes):
            num_friends = len(self.elem_nbrs[p])
            if num_friends == 2:
                elist.append(p)
        return elist

    def __repr__(self):
        rstring  = "system(["
        for bond in self.bonds:
            bstring = f'bond({bond.num},"{bond.nls}","{bond.nrs}","{bond.csd}", "{bond.ped}"),\n'
            rstring += bstring
        rstring += '])'
        return rstring

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
        elif self.name.startswith('I'):
            return 'I'
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

class elem_SF(element):
    def __init__(self, name):
        super().__init__(name)
        self.value = 'F(t)'
        self.f = self.value

class elem_SE(element):
    def __init__(self, name):
        super().__init__(name)
        self.value = 'E(t)'
        self.e = self.value

class elem_I(element):
    def __init__(self, name):
        super().__init__(name)
        self.value = 'p/I'
        self.f = self.value

class elem_C(element):
    def __init__(self, name):
        super().__init__(name)
        self.value = 'q/C'
        self.e = self.value

class elem_R(element):
    def __init__(self, name):
        super().__init__(name)
        self.value = 'R'
        self.e = self.value + '*f'
        self.f = 'e/'+self.value

class elem_TF(element):
    def __init__(self, name, b1, b2):
        super().__init__(name)
        self.value = 'm'

        # two ports
        self.p1 = {
                'e' : name+'.'+'p1.e',
                'f' : name+'.'+'p1.f',
                'b' : b1,
             }
        self.p2 = {
                'e' : name+'.'+'p2.e',
                'f' : name+'.'+'p2.f',
                'b' : b2,
             }
        # set working bond to p1.bond
        b = self.p1['b']

        # TF_elem is on right side
        if b.nrs == name:
            #print(f'[OK] NODE R is {e}')
            # check causal stroke direction
            #print(f'CS dir = {b.csd}')
                
            if b.csd == 'L':    
                #print('wow. Causal stroke is on the left!')    
                #print('TF is getting flow from the 1st bond')    
                self.p2['f'] = 'm*' + self.p1['f']    
                self.p1['e'] = 'm*' + self.p2['e']    

                # push values to bonds
                self.p2['b'].set_f(self.p2['f'])
                self.p1['b'].set_e(self.p1['e'])
            else:    
                #print('wowzer. cs is on the Right')
                #print('TF is getting effort from the 1st bond')
                self.p1['f'] = self.p2['f'] + '/m'
                self.p2['e'] = self.p1['e'] + '/m'

                # push values to bonds
                self.p1['b'].set_f(self.p1['f'])
                self.p2['b'].set_e(self.p2['e'])
                
        # TF_elem is on the left side
        else:
            #print(f'[OK] NODE L is {e}')
            #print(b)
            # check causal stroke direction
            #print(f'CS dir = {b.csd}')
            if b.csd == 'L':
                #print('wow. Causal stroke is on the left!')
                #print('TF is giving flow to the 1st bond')
                self.p1['f'] = self.p2['f'] + '/m'
                self.p2['e'] = self.p1['e'] + '/m'

                # push values to bonds
                self.p1['b'].set_f(self.p1['f'])
                self.p2['b'].set_e(self.p2['e'])
            else:
                #print('wowzer. cs is on the Right')
                #print('TF is giving effort to the 1st bond')
                self.p2['f'] = 'm*' + self.p1['f']
                self.p1['e'] = 'm*' + self.p2['e']

                # push values to bonds
                self.p2['b'].set_f(self.p2['f'])
                self.p1['b'].set_e(self.p1['e'])

class elem_0J(element):
    def __init__(self, name, bonds):
        super().__init__(name)
        self.bonds = bonds
        self.sb = self.get_sb()

        # set the efforts on each bond
        self.set_e()

        # store original flows
        self.tmp_fs = []
        for b in self.bonds:
            self.tmp_fs.append(b.f)

        # set the flows on each bond
        self.set_f()

    def print_bonds(self):
        for bond in self.bonds:
            if bond.nls == self.name:
                print(bond)
            else:
                print(bond.print_rev())

    # find strong bond
    def get_sb(self):
        self.sb = self.bonds[0]
        for bond in self.bonds:
            if bond.nls == self.name:
                if bond.csd == 'L':
                    self.sb = bond
            else:
                if bond.csd == 'R':
                    self.sb = bond
        return self.sb


    def set_e(self):
        for b in self.bonds:
            if b != self.sb:
                b.set_e(self.sb.e)

    def set_f(self):
        for b in self.bonds:
            fstring = ""
            s = self.sumfs(b)
            # is pos energy into 0J element?
            if b.is_ped_into_elem(self.name):
                fstring = "-("+s+")"
            else:
                fstring = "+("+s+")"
            b.set_f(fstring)

    def sumfs(self, bcurr):
        s = ""
        for i in range(len(self.bonds)):
            tmp_f = self.tmp_fs[i]
            b = self.bonds[i]
            if b != bcurr:
                if b.is_ped_into_elem(self.name):
                    s += " +"+"f_"+str(b.num)
                    #s += " +"+tmp_f
                else:
                    s += " -"+"f_"+str(b.num)
                    #s += " -"+tmp_f
        return s

class elem_1J(element):
    def __init__(self, name, bonds):
        super().__init__(name)
        self.bonds = bonds
        self.sb = self.get_sb()

        # set the flows on each bond
        self.set_f()  ## all same as sb

        # store original efforts
        self.tmp_es = []
        for b in self.bonds:
            self.tmp_es.append(b.e)

        # set the efforts on each bond
        self.set_e() # e = sumes

    def print_bonds(self):
        for bond in self.bonds:
            if bond.nls == self.name:
                print(bond)
            else:
                print(bond.print_rev())

    # find strong bond
    def get_sb(self):
        self.sb = self.bonds[0]
        for bond in self.bonds:
            if bond.nls == self.name:
                # [1J-L] ---| == SB
                if bond.csd == 'R':
                    self.sb = bond
            else:
                # |--- [1J-R]  == SB
                if bond.csd == 'L':
                    self.sb = bond
        return self.sb


    def set_f(self):
        for b in self.bonds:
            if b != self.sb:
                b.set_f(self.sb.f)


    def set_e(self):
        for b in self.bonds:
            fstring = ""
            s = self.sumes(b)
            # is pos energy into 1J element?
            if b.is_ped_into_elem(self.name):
                fstring = "-("+s+")"
            else:
                fstring = "+("+s+")"
            b.set_e(fstring)

    def sumes(self, bcurr):
        s = ""
        for i in range(len(self.bonds)):
            tmp_e = self.tmp_es[i]
            b = self.bonds[i]
            if b != bcurr:
                if b.is_ped_into_elem(self.name):
                    s += " +"+"e_"+str(b.num)
                    #s += " +"+tmp_e
                else:
                    s += " -"+"e_"+str(b.num)
                    #s += " -"+tmp_e
        return s

