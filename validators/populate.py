from biosamples import Biosamples


new_class = Biosamples()

print('I am the new class')
print(new_class)
print(type(new_class))
print(new_class.model_dump(exclude_none=True))
print(new_class.id)