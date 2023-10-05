def listRemoveDuplicates(source,filter):
    source = [x.lower() for x in source]
    filter = [x.lower() for x in filter]
    source.sort()
    filter.sort()
    filtered_list = source.copy()
    for i in source:
        if i in filter:
            filtered_list.remove(i) # <todo> not removing entry correctly
    return filtered_list

list_id = ["grade 4 artisanal skybuilders' astroscope", "grade 4 artisanal skybuilders' chocobo weathervane", "grade 4 artisanal skybuilders' company chest", "grade 4 artisanal skybuilders' icebox", "grade 4 artisanal skybuilders' sorbet", "grade 4 artisanal skybuilders' tincture", "grade 4 artisanal skybuilders' tool belt", "grade 4 artisanal skybuilders' vest", "grade 4 skybuilders' awning", "grade 4 skybuilders' bed", "grade 4 skybuilders' brazier", "grade 4 skybuilders' growth formula", "grade 4 skybuilders' lamppost", "grade 4 skybuilders' oven", "grade 4 skybuilders' overalls", "grade 4 skybuilders' stew"]
list_no_id = ["Grade 4 Skybuilders' Stew", "Grade 4 Skybuilders' Overalls"]

test = listRemoveDuplicates(list_no_id,list_id)
print(test)