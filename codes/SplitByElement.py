# -*- coding: utf-8 -*-

import sys, getopt
Elements = ['H', 'He', 'Li', 'Be', '', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 
    'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 
    'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 
    'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 
    'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 
    'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 
    'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Lr', 'Rf', 'Db', 'Sg', 
    'Bh', 'Hs', 'Mt', 'Ds', 'Rg']


 
def split_line(str):
    tmp = ''
    str+=' '
    i = 0
    while i <= len(str)-2:
#        print i
        sub = str[i: i+2]
        tmp_chr = 'x'
        if i<len(str)-2: tmp_chr = str[i+2]
        if sub in Elements and not (tmp_chr<'9' and tmp_chr>'0'or tmp_chr=='%'or tmp_chr=='x'):
#            print sub
            tmp+=(sub+' ')
            i = i+1
        elif str[i] == '%':
            tmp += (str[i: i+3]+' ')
            i = i+2
        else:
            tmp += (str[i]+' ')
        i += 1
    return tmp.strip().replace('  ', ' ')

def split_file(fin,fout):
    reader = open(fin, 'r+')
    writer = open(fout, 'w')
    try:
        while True:
            line = reader.readline()
            if not line: break
            line = split_line(line)
            writer.write(line+'\n')  
    finally:
        print('over')
        reader.close()
        writer.flush()
        writer.close()
    return  
    
def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,'hi:o:',['ifile=','ofile='])
    except getopt.GetoptError:
        print('SplitByElement.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('SplitByElement.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg
    print('inputfile:', inputfile)
    print('outputfile:', outputfile)
    split_file(inputfile,outputfile)


if __name__ == '__main__':
   main(sys.argv[1:])
