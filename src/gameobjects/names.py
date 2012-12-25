import village
modules = [village]

CLASSES = {}

for imported_module in modules:
    if hasattr(imported_module, 'BUILDER_NAMES'):
        CLASSES.update(getattr(imported_module, 'BUILDER_NAMES'))
