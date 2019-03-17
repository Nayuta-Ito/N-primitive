#Python版 Am schnellsteren (N1.1)

import copy

#拡張数列関係の定義
class ExtendedSequence:
    """Extended Sequence"""
    
    def __init__(self, term, non_principal):
        self.term = term
        self.non_principal = non_principal
        
    def __str__(self):
        return "["+str(self.term)+";"+str(self.non_principal)+"]"
    
    #(idx+1)番目の主要項が非主要項と合わせて(何+1)番目かを判定する
    def overall_term_count(self):
        len_term = length(self)
        if len_term > 0:
            ans = [len(self.non_principal[0])]
            for i in range(1, len_term):
                ans.append(ans[-1]+len(self.non_principal[i])+1)
            return ans
        else:
            return []

#「長さ」を返す
def length(self):
    if type(self) is ExtendedSequence:
        return len(self.term)
    else:
        return len(self)

#主要項の判定
def principal_pointers(list):
    """The places of principal terms"""
    n = len(list) - 1
    ans = [n]
    for i in range(n-1 , -1, -1):
        if list[i] > list[ans[-1]]:
            continue
        elif list[i] < list[ans[-1]]:
            ans.append(i)
        else:
            equal_flag = True
            if len(ans) <= 1:
                #print(i, "len(ans)<=1")
                equal_flag = False
            elif list[0] < 1:
                #print(i, "list[0]<1")
                equal_flag = False
            elif list[ans[-1]] >= list[-1]:
                #print(i, "list[ans[-1]] >= list[-1]")
                equal_flag = False
            else:
                #print(i, "else")
                equal_subflag = True
                if list[ans[-1]] >= list[ans[-2]]-1:
                    #print(i, "list[ans[-1]] >= list[ans[-2]]-1")
                    equal_subflag = False
                else:
                    for subi in range(ans[-1], ans[-2]):
                        if list[subi] != list[ans[-1]]:
                            equal_subflag = False
                if equal_subflag:
                    equal_flag = False
            if equal_flag:
                ans.append(i)
            else:
                continue
    return ans
    
#数列化
def to_a(self):
    len_term = length(self)
    len_non_principal = len(self.non_principal)
    len_max = max(len_term, len_non_principal)
    ans = []
    for i in range(0, len_max):
        if i < len_non_principal:
            ans += self.non_principal[i]
        if i < len_term:
            ans.append(self.term[i])
    return ans

#拡張化
def to_xs(self):
    pr_p = principal_pointers(self)
    length = len(self)
    term = []
    non_pr = []
    term_count = 0
    prev_term_flag = False
    for i in range(0, len(pr_p)):
        non_pr.append([])
    for i in range(0, length):
        if i in pr_p:
            prev_term_flag = True
            term_count += 1
            term.append(self[i])
        elif prev_term_flag:
            non_pr[term_count].append(self[i])
        else:
            non_pr[term_count].append(self[i])
    return ExtendedSequence(term, non_pr)

#階差数列
def difference(array):
    ans = []
    seq = array.term
    for i in range(0, len(seq)-1):
        ans.append(seq[i+1] - seq[i])
    return ans

#階差数列を限界まで取る
def difference_multiple(array):
    ans = []
    tmp = copy.deepcopy(array)
    while True:
        #print(array)
        tmp = to_xs(tmp)
        ans.append(tmp)
        tmp = difference(tmp)
        end_flag = True
        #「今見ている数列に末項より小さい項が存在する」かどうかを調べる
        for num in tmp:
            if num < tmp[-1]:
                end_flag = False
                break
        if end_flag:
            ans.append(to_xs(tmp))
            break
    return ans

#原始数列の展開
def expandPrim(array, base):
    length = len(array)
    ans = copy.deepcopy(array)
    b = -1
    for i in range(length-2, -1, -1):
        if array[i] < array[-1]:
            b = i
            break
    ans.pop()
    for itr in range(0, base):
        ans += array[b:-1]
    return ans
        
#N原始の展開
def expand(array, base):
    #後続配列
    if array[-1] == 0:
        return None
    
    #例外規則
    if array == [0,1]:
        return [0 for i in range(base+1)]
    
    #基本規則
    #階差フェーズ
    a = difference_multiple(array)
    for exseq in a:
        print(exseq)
    k = len(a)
        
    #簡単のため選定フェーズを先に行う
    star_pointer = [0]
    star_pointer.append(a[-1].overall_term_count()[0])
    for i in range(len(a)-3, -1, -1):
        #(above's pointer's overall index)+1th entry
        isum=a[i+1].overall_term_count()[star_pointer[-1]]+1
        star_pointer.append(isum)
    star_pointer.reverse()
    print("star_pointer:",star_pointer)
    
    #展開フェーズ
    #(bad partの長さ*n)段まで計算する
    c = []
    for exseq in a:
        c.append(exseq.term[0])
    bad_length = len(array) - star_pointer[0] 
    #これだけ用意すれば長さが足りるだろう
    c = expand(c, (bad_length - 1) * base + len(star_pointer))
    print("c:",c)
    
    #構築フェーズ
    #帰納フェーズ
    induction = [[c[-1]]]
    count_for_induction_index = 1
    #from the second-to-last entry to the next of (a's length) (inclusive to)
    for i in range(len(c)-2, len(a)-1, -1):
        row = [c[i]]
        for j in range(1, count_for_induction_index+1):
            #print(i,j)
            row.append(row[-1]+induction[count_for_induction_index-1][j-1])
        induction.append(row)
        count_for_induction_index += 1
        #print(induction)
    induction.reverse()
    a += induction
    print("induction:",induction)
    
    #超限フェーズ
    pdash = 0
    qdash = 0
    for m in range(k-1, -1, -1):
        print("---", "m=", m, "---")
        if type(a[m+1]) is ExtendedSequence:
            print("a[m+1]:",a[m+1])
            a[m+1] = to_a(a[m+1])
        p = length(a[m])-1
        q = p - star_pointer[m]
        print("p,q:",p,q)
        if m==0:
            pdash = len(to_a(a[0])) - 1
            qdash = pdash - a[0].overall_term_count()[star_pointer[0]]
        if p==0:
            a[m].term[p] = c[m]
            q = 1
        i = max(p,1)
        #「無限に繰り返す」とあるが、(a[m+1]の項数+1)項目まで計算する
        while True:
            if i >= len(a[m+1]):
                break
            
            while length(a[m]) < i+1:
                a[m].term.append(0)
            while length(a[m].non_principal) < i+1:
                a[m].non_principal.append([])
                
            a[m].term[i] = a[m].term[i-1] + a[m+1][i-1]
            
            if i > max(p,1):
                if p==0 or i-q < p:
                    a[m].non_principal[i] = []
                else:
                    a[m].non_principal[i] = copy.deepcopy(a[m].non_principal[i-q])
                    
                    for j in range(0, len(a[m].non_principal[i])):
                        #i-q>=0であることは7行上のif文で保障されている
                        amiqj = a[m].non_principal[i-q][j]
                        ami1 = a[m].term[i-1]
                        ami1q = a[m].term[i-1-q]
                        di = a[m+1][i] #a[m+1]はList
                        diq = a[m+1][i-q]
                        a[m].non_principal[i][j] = amiqj + ami1 - ami1q + di - diq
            print("i:",i)
            print("a[m+1]:",a[m+1])
            print("a[m]:",a[m])
            i += 1
    a[0] = to_a(a[0])
    print("p',q':", pdash, qdash)
    return a[0][:(pdash + base * qdash)]
    
list = [0,1,2,3,2]
base = 3
'''
#乱数で値を入れる。「ある程度の」確率で原始数列の標準形が現れる。
import random
for i in range(0,10):
    list.append(list[random.randint(0,i)]+1)
print(list) #expandがバグった時用
'''
a = expand(list, base)
print(list)
print(a)
'''
print(expandPrim(list,5))
xs = to_xs(list)
dif_mul = difference_multiple(list)
for i in range(0, len(dif_mul)):
    print(dif_mul[i])
'''