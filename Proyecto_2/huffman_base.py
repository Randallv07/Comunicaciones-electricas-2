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

#-----------------------------------------------------------
#-                2.2-ALGORITMO DE HUFFMAN       -
#-----------------------------------------------------------
#Apertura y lectura del archivo
string=[]
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
    

# Calculo de frecuencias y probabilidades
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

n_orig = H/8       #Se calcula la eficiencia con el código original, los caracteres siempre son de 8 bits

if L==0:
    n_new = "No aplica ya que solo se está enviando un único caracter"
else:
    n_new  = H/L   #Se calcula la eficiencia del código nuevo 


print("-La entropia de la fuente es:",H)    # Se muestra el valor de la entropia de la fuente
print("-La longitud media del código es:",L) # Se muestra el valor de la longitud promedio del codigo nuevo
print("-La varianza del código es:",sigma)  #Se muestra la varianza del código nuevo
print("-La eficiencia del código original:",n_orig) #Se muestra la eficiencia del código original
print("-La eficiencia de nuevo código:",n_new) #Se muestra la eficiencia del código nuevo


#-----------------------------------------------------------
#-      2.3-COMPRESION POR MEDIO DEL CODIGO DE HUFFMAN        -
#-----------------------------------------------------------

binary_string = []
for c in string:
    binary_string += huffmanCode[c]

compressed_length_bit = len(binary_string)

if(compressed_length_bit %8>0):
    for i in range(8 - len(binary_string) % 8):
        binary_string += '0'

byte_string="".join([str(i) for i in binary_string])
byte_string=[byte_string[i:i+8] for i in range(0, len(byte_string), 8)]



lista_bytes = [byte.encode() for byte in byte_string]   #Convierte los datos comprimidos a una lista de datos tipo byte

#Genera el archivo .bin
with open(file_huffman_comprimido, 'wb') as archivo_binario:
    for byte in lista_bytes:
        archivo_binario.write(byte)

#Genera el archivo csv
csvfile = open ( ruta_diccionario , 'w')
writer = csv.writer ( csvfile )
writer . writerow ([ str ( compressed_length_bit ) ,"bits"])

for entrada in huffmanCode :
   writer.writerow ([str(entrada) , huffmanCode [ entrada ]])

csvfile.close ()


#Se guarda el valor del tamaño del archivo original y el de el archivo comprimido
tamaño_original = os.path.getsize(file_full_path) 
print("-El tamaño original del archivo es:", tamaño_original, "bytes")
tamaño_new = math.floor(compressed_length_bit/8)   #Pasa el tamaño a bytes
print("-El tamaño del archivo comprimido es",tamaño_new,"bytes")


#Condición por si no hay tasa de compresión
if tamaño_original == tamaño_new:
    tasa_compress = "-No hay tasa de compresión ya que no se comprime el archivo porque solo se transmite un caracter"
    print(tasa_compress)
else:
    tasa_compress = tamaño_new/tamaño_original  #Se calcula la tasa de compresión
    print("-La tasa de compresión es del : ", tasa_compress )



#-----------------------------------------------------------
#-    2.4-RESTABLECIMIENTO DE LOS DATOS ORIGINALES-DESCOMPRESIÓN        -
#-----------------------------------------------------------    
csvfile = open ( ruta_diccionario , 'r')
reader = csv.reader(csvfile)
bits_a_leer = None
diccionario = dict ()

for row in reader:
    if (bits_a_leer ==None):
        bits_a_leer = int(row[0])

    else:
        diccionario.update ({int(row[0]):row[1]})

Decoding = NodeTree (None, None)
for entrada in diccionario:
    insert_in_tree(Decoding, diccionario[entrada], entrada)

nodo = Decoding
data_estimated = []
for i in range (compressed_length_bit):
    (l,r) = nodo.children ()
    #print ([i , binary_string[i]])
    if (binary_string[i] == '1'):
        nodo = r
    else:
        nodo = l
    
    if type(nodo) is int:
        data_estimated.append(nodo)
        #print([i, nodo])
        nodo = Decoding


if string==data_estimated:
    print("Los datos estimados corresponden a los datos originales de la fuente")
else:
    print("Los datos no corresponden")


#Se convierten los datos estimados a bytes
estimado_bin = []

for i in data_estimated:
    estimado_bin.append(i.to_bytes(1, byteorder='big'))

#Genera el archivo recuperado
with open(recovered_path, 'wb') as archivo_binario:
    for byte in estimado_bin:
        archivo_binario.write(byte)


#-----------------------------------------------------------
#-      2.5-EFECTO DE LA ENTROPÍA EN LA FUENTE        -
#-----------------------------------------------------------

#Este punto fue elaborado apartir de ejecutar el código desarrollado en consola e ingresar como parámetro
# el archivo que se desea comprimir.
# El resultado obtenido se muestra en el informe de igual forma que las respuestas a las preguntas de teoria
