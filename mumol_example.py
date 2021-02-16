from os import read
import sys
import mumol

input_file=open("data/50mols.sdf",  "rb")
text=input_file.read(4096).decode("ascii")
print(text.find("$$$$"))
mol_text=text[:text.find("$$$$")+4]
print(mol_text)
molbytes=mumol.sdf_text_to_bytes(mol_text)
print(molbytes)
print(len(mol_text))
print(len(molbytes))
print(len(molbytes)/len(mol_text)*100, "%")
import zlib
print(len(zlib.compress(mol_text.encode("utf-8"),9)))
print(len(molbytes)/len(zlib.compress(mol_text.encode("utf-8"),9))*100, "%")
