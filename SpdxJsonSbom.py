
from GenericSbom import GenericSbom
import json
import SbomTypes

class SpdxJsonSbom(GenericSbom):

    packages = None
    files = None
    relationships = None
    product = None

    def get_packages(self):
        return self.packages

    def get_files(self):
        return self.files
    
    def get_final_product(self):
        return self.product


    def nodeToPackage(self, pkg):
        p = SbomTypes.Package()
        
        p.id = pkg['SPDXID']
        p.name = pkg['name']

        if 'versionInfo' in pkg:
            p.version = pkg['versionInfo']
        
        if 'supplier' in pkg:
            p.supplierName = pkg['supplier']
        
        return p
        

    def nodeToRelationship(self, rel):
        r = SbomTypes.Relationship()

        r.fromId = rel['spdxElementId']
        r.toId = rel['relatedSpdxElement']
        r.type = rel['relationshipType']

        return r

    def nodeToFile(self, fil):
        
        f = SbomTypes.File()

        f.name = fil['fileName']
        f.id = fil['SPDXID']

        if 'checksums' in fil:
            hashes = []
            for cc in fil['checksums']:
                h = SbomTypes.Hash()
                h.algo = cc['algorithm']
                h.value = cc['checksumValue']
                hashes.append(h)
            f.hash = hashes


    def __init__(self, infile):
        self.fileName = infile
        with open(infile) as fh:
            data = json.load(fh)

            if 'packages' in data:
                self.packages = []
                for p in data['packages']:
                    self.packages.append(self.nodeToPackage(p))
            
            if 'relationships' in data:
                self.relationships = []
                for r in data['relationships']:
                    self.relationships.append(self.nodeToRelationship(r))
            

            if 'files' in data:
                self.files = []
                for f in data['files']:
                    self.relationships.append(self.nodeToFile(f))
        

if __name__ == '__main__':
    x = SpdxJsonSbom('./inputs/Tern/simple_container/hello_world_linux_spdx.json.txt')


    x = SpdxJsonSbom('./inputs/Synopsys Black Duck/libresolar-zephyr/plugfest-libresolar-source-sbom-plugfest.spdx.json')

    x.dump()

