t forbes brown
✓ 
✓
✗

[✓] SE
[✓] I
[✓] SF
[✓] R
[✓] C

[ ] TF
[ ] 0J
[ ] 1J

element = {
  type = {
    SE
    SF
    R
    C
    I
    TF
    0J
    1J
  }
  nports = {
    1
    2
    n
  }
  bonds = {
  }
  gives = {
    e
    f
  }
}



single-port elements

IF name[0] == 'S':

# SE  ___|
  e = E

# SF |___
  f = F

# R   ___|
  e = R f    (PREFERRED)
# R  |___
  f = e / R

# C   ___|
  e = q / c  (PREFERRED)
# C  |___
  f = qdot

# I   ___|
  e = pdot
# I  |___
  f = p / I  (PREFERRED)

# |_1_ TF |_2_
    e1 = m e2
  m f1 = f2
#  _1_| TF _2_|
    f1 = f2 / m
    e1 / m = e2

# _1_| 0 _2_|
       |
       3
       |
       _
  e2 = e1
  e3 = e1
  f1 = -(f2+f3)

# _1_| 1 _2_|
       |
       3
       |
       _
  f2 = f1
  f3 = f1
  e1 = -(e2+e3)


#  node-left: SE
#  node-right: 1J-5
#  stroke-side: Right

BOND
NL -- N  -- NR

if (CS:R)
  NL  -- N  -- |NR
else
  NL| -- N  --  NR

if (POS-E: L)
  NL /-- N  -- NR
else
  NL  -- N  --\NR


bond (node-left, node-right, stroke-dir, pos-e-dir, num)
bond( 14 ,   'SE', '1J-5 '  , 'R' , 'L')
bond( 15 ,    'I', '1J-5 '  , 'L' , 'L')
bond( 14 , '1J-5', 'TF.Ab'  , 'L' , 'L')
bond( 13 ,'TF.Ab', '1J-4 '  , 'L' , 'L')
bond( 12 ,   'Rb', '1J-4 '  , 'R' , 'L')


01234567890123456789012345
[NodeL] |<__nn__>| [NodeR]
[1J-5 ] | __17__>  [TF.an]
[TF.an] | __18__>  [1J-6 ]
[Ra   ]  <__19__ | [1J-6 ]
[1J-6 ] | __20__>  [Rv70 ]
[1J-6 ] | __21__>  [Rv20 ]
[1J-6 ] | __22__>  [0J-1 ]

 12345              12345
[SE   ]  <__16__ | [1J-5 ]
[1J-4 ] |<__11__   [0J-1 ]
[0J-1 ] | __10__>  [1J-3 ]
[Rv40 ]  <__ 9__ | [1J-3 ]
[1J-3 ] | __ 8__>  [Rl40 ]
[1J-3 ] | __ 7__>  [0J-2 ]
[1J-2 ] | __ 6__>  [Cacc1]
[Rp2  ]  <__ 5__ | [1J-2 ]
[0J-2 ] | __ 4__>  [1J-2 ]
[0J-2 ]   __ 3__>| [1J-1 ]
[1J-1 ]   __ 2__>| [Rp3  ]
[1J-1 ] | __ 1__>  [Cacc2]



bonds.append(bond.from_bond_string('[1J-5 ] | __17__>  [TF.an]' )
bonds.append(bond.from_bond_string('[TF.an] | __18__>  [1J-6 ]' )
bonds.append(bond.from_bond_string('[Ra   ]  <__19__ | [1J-6 ]' )
bonds.append(bond.from_bond_string('[1J-6 ] | __20__>  [Rv70 ]' )
bonds.append(bond.from_bond_string('[1J-6 ] | __21__>  [Rv20 ]' )
bonds.append(bond.from_bond_string('[1J-6 ] | __22__>  [0J-1 ]' )

bonds.append(bond.from_bond_string('[SE   ]  <__16__ | [1J-5 ]' )
bonds.append(bond.from_bond_string('[1J-4 ] |<__11__   [0J-1 ]' )
bonds.append(bond.from_bond_string('[0J-1 ] | __10__>  [1J-3 ]' )
bonds.append(bond.from_bond_string('[Rv40 ]  <__ 9__ | [1J-3 ]' )
bonds.append(bond.from_bond_string('[1J-3 ] | __ 8__>  [Rl40 ]' )
bonds.append(bond.from_bond_string('[1J-3 ] | __ 7__>  [0J-2 ]' )
bonds.append(bond.from_bond_string('[1J-2 ] | __ 6__>  [Cacc1]' )
bonds.append(bond.from_bond_string('[Rp2  ]  <__ 5__ | [1J-2 ]' )
bonds.append(bond.from_bond_string('[0J-2 ] | __ 4__>  [1J-2 ]' )
bonds.append(bond.from_bond_string('[0J-2 ]   __ 3__>| [1J-1 ]' )
bonds.append(bond.from_bond_string('[1J-1 ]   __ 2__>| [Rp3  ]' )
bonds.append(bond.from_bond_string('[1J-1 ] | __ 1__>  [Cacc2]' )


N0
|
+-- N1
|
+-- N2
|
+-- N3
|
+-- N4
|
+-- N5


edge properties
  num
  nls
  nrs
  csd [LR]
  ped [LR]


# make a dict with all the nodes from the bonds





