import os
import sys
import getopt
import csv
import math
from math import log2

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

# Entropia de la fuente

Hent = 0
for i in range(len(freq)):
    Hent = Hent + freq[i][1]*log2(1/freq[i][1])

# Longitud media del codigo Huffman generado

Lprom = 0
for (char, frequency) in freq:
    Lprom = Lprom + frequency*len(huffmanCode[char])

# Varianza del codigo de Huffman 

Var = 0
for (char, frequency) in freq:
    Var = Var + frequency*(len(huffmanCode[char])-Lprom)**2

# Eficiencia de la codificacion original

eta_o = 0
for (char, frequency) in freq:
    eta_o =  Hent/8

# Eficiencia del nuevo codigo

eta_n = 0
for (char, frequency) in freq:
    if Lprom==0:
        eta_n = "NA"
    else:
        eta_n = Hent/Lprom

print(' Char | Huffman code ')
print('----------------------')
for (char, frequency) in freq:
    print(' %-4r |%12s' % (char, huffmanCode[char]))

print("\n")
print("La entropía es            :", Hent)
print("La longitud promedio es   :", Lprom)
print("La varianza es            :", Var)
print("La eficiencia original es :", eta_o)
print("La eficiencia nueva es    :", eta_n)
print("\n")


#-----------------------------------------------------------
#-       COMPRESION POR MEDIO DEL CODIGO DE HUFFMAN        -
#-----------------------------------------------------------

##############################
# Codigo para el punto 2.3.1 #
##############################

binary_string = []
for c in string:
    binary_string += huffmanCode[c]

compressed_length_bit = len(binary_string)

if(compressed_length_bit %8>0):
    for i in range(8 - len(binary_string) % 8):
        binary_string += '0'

byte_string="".join([str(i) for i in binary_string])
byte_string=[byte_string[i:i+8] for i in range(0, len(byte_string), 8)]

# Codigo para el punto 2.3.2
binary_bytes = [byte.encode() for byte in byte_string]

with open(file_huffman_comprimido,'wb') as archivo_binario:
    for byte in binary_bytes:
        archivo_binario.write(byte)

##############################
# Codigo para el punto 2.3.3 #
##############################

csvfile = open(ruta_diccionario, 'w')
writer = csv.writer(csvfile)
writer.writerow([str(compressed_length_bit), "bits"])

for entrada in huffmanCode:
    writer.writerow([str(entrada), huffmanCode[entrada]])

csvfile.close()

##############################
# Codigo para el punto 2.3.4 #
##############################

original_size = os.path.getsize(file_full_path)
compress_size = math.floor(compressed_length_bit/8)

if original_size==compress_size:
    tasa = "No se realiza compresión"
else:
    tasa = compressed_length_bit/(original_size*8)

print("El tamaño original en bytes es        :", original_size)
print("El tamaño de la versión comprimida es :", compress_size)
print("La tasa de compresión es              :", tasa)

#---------------------------------------------------------
#-                      DESCOMPRESION                    -
#---------------------------------------------------------


##############################
# Codigo para el punto 2.4.1 #
##############################

csvfile = open(ruta_diccionario, 'r')
reader = csv.reader(csvfile)
bits_a_leer = None
diccionario = dict()

for row in reader:
    if(bits_a_leer==None):
        bits_a_leer = int(row[0])
    else:
        diccionario.update({int(row[0]): row[1]})

Decoding = NodeTree(None,None)
for entrada in diccionario:
    insert_in_tree(Decoding, diccionario[entrada],entrada)

nodo = Decoding
data_estimated = []
for i in range(compressed_length_bit):
    (l,r) = nodo.children()
    #print([i,binary_string[i]])
    if(binary_string[i]=='1'):
        nodo = r
    else:
        nodo = 1

    if type(nodo) is int:
        data_estimated.append(nodo)
        #print([i, nodo])
        nodo = Decoding

