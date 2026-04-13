import fitz

doc = fitz.open()
print([x for x in dir(doc) if 'image' in x.lower()])
