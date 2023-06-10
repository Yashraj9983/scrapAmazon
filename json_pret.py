import json
import sys
try:
    fname=sys.argv[1]
    try:
        if fname.split('.')[1]=='json':
            f=open(fname)
            data=json.load(f)
            pret_fname=fname.split('.')[0]+'_pret.json'
            with open(pret_fname, 'w') as outfile:
                json.dump(data,outfile,indent=4,ensure_ascii=False)
            print("saved as ",pret_fname)    
        else: 
            print("not a json file")        
    except:
        print("not a json file2")                
except:
    print("no file specified")