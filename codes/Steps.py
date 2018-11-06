# -*- coding: utf-8 -*-
'''
Find the longest common sequence (LCS)

Created on Mon Jul 10 15:45:59 2017

@author: jshmjs45
'''

import SplitByElement

def getLCS(X, Y):   
    s1 = X.split(' ')
    s2 = Y.split(' ')
    m = [ [ 0 for x in range(len(s2)+1) ] for y in range(len(s1)+1) ]   
    d = [ [ None for x in range(len(s2)+1) ] for y in range(len(s1)+1) ]   
  
    for p1 in range(len(s1)):   
        for p2 in range(len(s2)):   
            if s1[p1] == s2[p2]:
                m[p1+1][p2+1] = m[p1][p2]+1  
                d[p1+1][p2+1] = 'ok'            
            elif m[p1+1][p2] > m[p1][p2+1]:
                m[p1+1][p2+1] = m[p1+1][p2]   
                d[p1+1][p2+1] = 'left'            
            else: 
                m[p1+1][p2+1] = m[p1][p2+1]     
                d[p1+1][p2+1] = 'up'           
    (p1, p2) = (len(s1), len(s2))   
 
    s = []   
    while m[p1][p2]:   
        c = d[p1][p2]  
        if c == 'ok':  
            s.append(s1[p1-1]+' ')  
            p1-=1  
            p2-=1   
        if c =='left':  
            p2 -= 1  
        if c == 'up':    
            p1 -= 1  
    s.reverse()   
    return ''.join(s)  
	
deleteIndex = []
addIndex = []
deleteString = []
addString = []


def record_steps(x,y,lcs):
    lcs = lcs.replace('  ', ' ')
    x_index = 0
    y_index = 0
    lcs_index = 0
    deleteIndex[:]=[]
    addIndex[:]=[]
    deleteString[:]=[]
    addString[:]=[]
    	
    x_strs = x.split(' ')
    y_strs = y.split(' ')
    lcs_strs = lcs.split(' ')
    	
    while x_index < len(x_strs)or y_index < len(y_strs):
#        print(lcs_index)
        if lcs_index >= len(lcs_strs) or x_index==len(x_strs) or y_index==len(y_strs):
            i = y_index
            while i < len(y_strs):
#                print 'add '+y_strs[y_index]+' at '+str(x_index)
                addString.append(y_strs[y_index])
                addIndex.append(x_index)
                y_index+=1
                i+=1
                
            i = x_index    
            while i < len(x_strs):
#                print 'delete '+x_strs[x_index]+' at '+str(x_index)				
                deleteString.append(x_strs[x_index])
                deleteIndex.append(x_index)
                x_index+=1
                i+=1
            break
        
        elif not x_strs[x_index]==y_strs[y_index]:
            if not y_strs[y_index]==lcs_strs[lcs_index]:
#                print('add '+y_strs[y_index]+' at '+str(x_index)) 
                addString.append(y_strs[y_index])
                addIndex.append(x_index)
                y_index+=1
            if not x_strs[x_index]==lcs_strs[lcs_index]:
#                print('delete '+x_strs[x_index]+' at '+str(x_index))
                deleteString.append(x_strs[x_index])
                deleteIndex.append(x_index)
                x_index+=1

        else:
            x_index+=1
            y_index+=1
            lcs_index+=1

def combine_addsteps():
    add_string = []      
    add_pos = []
    steps = ''
    front = -1
    now = -1
    addStart = 0
    addBuffer = ''
    global addIndex
    global addString

    i = 0
    while i<len(addIndex): 
        now = addIndex[i]
        if now==front:
            addBuffer += addString[i]
        elif now-front == 1 and front in deleteIndex:
            addBuffer += addString[i]
        else:
            if not addBuffer == '':
                step = '+ '+addBuffer+' '+str(addStart)
                steps += step+'\n'
#                print(step)
                add_string.append(addBuffer)
                add_pos.append(addStart)
            addBuffer = addString[i]
            addStart = now
        front = now
        i+=1
        
    if not addBuffer == '':
        step = '+ '+addBuffer+' '+str(addStart)
        steps += step+'\n'
#        print(step)
        add_string.append(addBuffer)
        add_pos.append(addStart)

    addIndex = add_pos
    addString = add_string
#    print steps
#    print addIndex
#    print addString
    return steps        

def trans_line(x,y):
    lcs = getLCS(x,y)
    record_steps(x,y,lcs)
    combine_addsteps()
    x_strs = x.split(' ')
    out = ''
    tmp = []
    for i in range(len(addString)):
        tmp_str = SplitByElement.split_line(addString[i])
        tmp.append(tmp_str)

    for i in range(len(x_strs)+1):
        if i in addIndex and not i in deleteIndex:
            step = tmp[addIndex.index(i)]
            out += (step+' AD ')
        if not i in addIndex and i in deleteIndex:
            out += ('RR'+' ')
        if not i in addIndex and not i in deleteIndex:
            out += ('_'+' ')
        if i in addIndex and i in deleteIndex:
            step = tmp[addIndex.index(i)]
            out += (step+' AR ')

#    print(out)
    return out.replace('  ', ' ')

def trans_file(fin):
    reader = open(fin, 'r+')
    writer1 = open(fin+'.l', 'w')
    writer2 = open(fin+'.r', 'w')
    writer3 = open(fin+'.steps', 'w')
    try:
        while True:
            line = reader.readline()
            if not line: break
            strs = string.split(line,'>>')
            if not len(strs) == 2: continue 
            line_l = strs[0]
            line_r = strs[1]
            line_l = SplitByElement.split_line(line_l)
            line_r = SplitByElement.split_line(line_r)
            trans = trans_line(line_r,line_l)
            writer1.write(line_l+'\n')
            writer2.write(line_r+'\n')
            writer3.write(trans+'\n')
    finally:
        print('over')
        reader.close()
        writer1.flush()
        writer1.close()
        writer2.flush()
        writer2.close()
        writer3.flush()
        writer3.close()
    return  


#x = 'N c x c c c ( Cl ) n c x'
#y = 'Cl c x c c c ( c n x ) N ( = O ) = O'
#print trans_line(x,y)
