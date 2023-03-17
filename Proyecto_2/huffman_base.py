import os
import sys
import getopt
import csv
from math import log2
import struct

# Parametros de entrada y ayuda:
file_full_path = ""
file_split_path = [];
def myfunc(argv):
    global file_full_path, file_split_path
    arg_output = ""
    arg_user = ""
    arg_help = "{0} -i <input>".format(argv[0])
    
    try:
        opts, args = getopt.getopt(argv[1:], "hi:", ["help", "input="])
    except:
        print(arg_help)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  
            sys.exit(2)
        elif opt in ("-i", "--input"):
            file_full_path = arg
            file_split_path = os.path.normpath(file_full_path)
            file_split_path = os.path.split(file_split_path)


if __name__ == "__main__":
    myfunc(sys.argv)


file_huffman_comprimido = file_full_path+".huffman"
ruta_diccionario = file_full_path+".diccionario.csv"
recovered_path = os.path.join(file_split_path[0], "recovered_"+file_split_path[1]);
#-----------------------------------------------------
# Algorithmo de compresión de huffman
#-----------------------------------------------------
#Apertura y lectura del archivo
string=[];
with open(file_full_path, "rb") as f:
    while (byte := f.read(1)):
        # Do stuff with byte.
        int_val = int.from_bytes(byte, "big")
        string.append(int_val)

# Árbol binario
class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
    def children(self):
        return (self.left, self.right)
    def nodes(self):
        return (self.left, self.right)
    def __str__(self):
        return '%s_%s' % (self.left, self.right)

def insert_in_tree(raiz, ruta, valor):
    if(len(ruta)==1):
        if(ruta=='0'):
            raiz.left = valor;
        else:
            raiz.right = valor;
    else:
        if(ruta[0]=='0'):
            #if type(raiz.left) is int:
            if(raiz.left==None):
                raiz.left = NodeTree(None,None);
            ruta = ruta[1:];
            insert_in_tree(raiz.left,ruta,valor);
        else:
            #if type(raiz.right) is int:
            if(raiz.right==None):
                raiz.right = NodeTree(None,None);
            ruta = ruta[1:];
            insert_in_tree(raiz.right,ruta,valor);


# Función principal del algoritmo de Huffman
def huffman_code_tree(node, left=True, binString=''):
    if type(node) is int:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d
    

# calculo de frecuencias y probabilidades
prob_unit = 1/len(string)
freq = {}
for c in string:
    if c in freq:
        freq[c] += prob_unit
    else:
        freq[c] = prob_unit

freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)


nodes = freq

while len(nodes) > 1:
    (key1, c1) = nodes[-1]
    (key2, c2) = nodes[-2]
    nodes = nodes[:-2]
    node = NodeTree(key1, key2)
    nodes.append((node, c1 + c2))
    #print(nodes)
    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

huffmanCode = huffman_code_tree(nodes[0][0])

print(' Char | Huffman code ')
print('----------------------')
H=0
L=0

for (char, frequency) in freq:
    print(' %-4r |%12s' % (char, huffmanCode[char]))
    H = frequency*log2(1/frequency)+H       #Se calcula la entropia de la fuente
    L = frequency*len(huffmanCode[char])+L  #Se calcula lo longitud promedio de la codificación de Huffmann
    

sigma=0
for (char, frequency) in freq:
    sigma = frequency*(len(huffmanCode[char])-L)**2+sigma  #Se calcula la varianza del código

n_orig = H/8       #Se calcula la eficiencia con el código original, los caracy¿teres siempre son de 8 bits

if L==0:
    n_new = "No aplica ya que solo se está enviando un único caracter"
else:
    n_new  = H/L       #Se calcula la eficiencia del código nuevo 


print("La entropia de la fuente es:",H)
print("La longitud media del código es:",L)
print("La varianza del código es:",sigma)
print("La eficiencia del código original:",n_orig)
print("La eficiencia de nuevo código:",n_new)

binary_string = [];
for c in string :
    binary_string += huffmanCode[c]

compressed_length_bit = len(binary_string)
if (compressed_length_bit %8 >0) :
    for i in range(8 - len(binary_string) % 8):
        binary_string += '0'
        
byte_string="".join ([str(i) for i in binary_string])
byte_string=[byte_string[i:i+8] for i in range (0, len(byte_string),8)];

Lista_byte = [byte.encode() for byte in byte_string]

with open(file_huffman_comprimido, 'wb') as archivo_binario:
    for byte in Lista_byte:
        archivo_binario.write(byte)

#print(Lista_byte)
print(type(Lista_byte[1]))

sin_compresion = len(string)

csvfile=open(ruta_diccionario,'w')
writer=csv.writer(csvfile)
writer.writerow([str(compressed_length_bit/8),"bits comprimidos"])
writer.writerow([str(sin_compresion),"bits sin comprimir"])
writer.writerow([str((compressed_length_bit/8)/sin_compresion*100)," por ciento de tasa de compresión"])

for entrada in huffmanCode :
    writer.writerow([str(entrada), huffmanCode[entrada]])
    
csvfile . close ()