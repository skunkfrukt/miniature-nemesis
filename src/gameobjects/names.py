import village
modules = [village]

CLASSES = {}

for imported_module in modules:
    if hasattr(imported_module, 'BUILDER_NAMES'):
        CLASSES.update(getattr(imported_module, 'BUILDER_NAMES'))
    '''for class_name in dir(imported_module):
        if hasattr(imported_module, class_name):
            imported_class = getattr(imported_module, class_name)
            print 'Trying {}'.format(class_name)
            if hasattr(imported_class, 'BUILDER_NAME'):
                builder_name = getattr(imported_class, 'BUILDER_NAME')
                CLASSES[builder_name] = imported_class'''

print CLASSES
