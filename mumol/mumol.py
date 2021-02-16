import struct
import zlib
atom_type_dict={"H":0, "C":1, "N":2 ,"O":3, "S":4, "F":5, "Cl":6, "Br":7, "I":8, "B":9, "P":10, "Si":11}
#Title length (max 255) chars
#Title chars of length "title length"
#UnsignedCharNumAtoms
#UnsignedCharNumBonds
#Floats, (x,y,z)*numatoms
#unsigned chars bond_from,bond_to,bond_order
def sdf_text_to_bytes(sdf_text:str, compress:bool=False):
    fmt="B"
    sdf_lines=sdf_text.splitlines()
    title=sdf_lines[0]
    fmt+=str(len(title))+"s"
    num_atoms=int(sdf_lines[3][0:4])
    num_bonds=int(sdf_lines[3][4:6])
    assert num_atoms<256, "Too many atoms to represent in the µMol format"
    assert num_bonds<256, "Too many bonds to represent in this format"
    fmt+="BB" # Num atoms and bonds
    atoms=[]
    for atom_num in range(num_atoms):
        line=sdf_lines[4+atom_num]
        x=float(line[0:10])
        y=float(line[11:21])
        z=float(line[21:30])
        atom_type=atom_type_dict[line[31:33].strip()]
        fmt+="e"*3+"B"
        atoms.append((x,y,z, atom_type))
    bonds=[]
    for bond_num in range(num_bonds):
        line=sdf_lines[4+num_atoms+bond_num]
        bond_from=int(line[0:3])
        bond_to=int(line[3:6])
        bond_order=int(line[6:10])
        bonds.append((bond_from, bond_to, bond_order))
        fmt+="B"*3
    molbytes=bytearray(struct.calcsize(fmt))
    molecule_struct=[len(title)]
    molecule_struct.append(title.encode("ascii"))
    molecule_struct.append(num_atoms)
    molecule_struct.append(num_bonds)
    for atom in atoms:
        molecule_struct.extend([atom[0],atom[1],atom[2],atom[3]])
    for bond in bonds:
        molecule_struct.extend([bond[0],bond[1],bond[2]])

    struct.pack_into(fmt,molbytes,0,*molecule_struct)
    if compress:
        return zlib.compress(molbytes,9)
    else:
        return molbytes
    