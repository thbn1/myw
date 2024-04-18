import cProfile

def isdgt(s):
    try:
        z=int(s)
        print(z)
    except:
        z=1
        print(z)


if __name__== '__main__':
    cProfile.run(isdgt("asd"))
