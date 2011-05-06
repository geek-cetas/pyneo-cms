import db

class Field(object):
    pass

class TypeField(Field):
    def __init__(self, _type, default=None):
        self._val_default = default
        self.value = _type(default)
        self._type = _type

    def __str__(self):
        return str(self.value)

    def __setattr__(self, key, val):
        if key == 'value':
            if hasattr(self, '_type'):
                val = self._type(val)

        object.__setattr__(self, key, val)

class RelationField(Field):
    def __init__(self, cls, relation = 'KNOWS', direction = 'Undirected'):
        self.relation = str(relation)
        self.direction = str(direction)
        self._cls = cls

    def __setattr__(self, key, val):
        if key == 'value':
            if not isinstance(val, self._cls):
                raise Exception("Invalid related node")
        object.__setattr__(self, key, val)

class TextField(TypeField):
    def __init__(self, default=None):
        super(TextField, self).__init__(str, default)

class Model(db.Node):
    def __init__(self, **kwargs):

        id = kwargs.get('id')
        if id:
            super(Model, self).__init__(id = id)
        else:
            init_vals = {}

        for field in dir(self):
            if '__' in field: continue

            val = getattr(self, field)
            if id and isinstance(val, RelationField):
                setattr(self, field, self.getRelations(val.relation,
                                                        val.direction))
            if not isinstance(val, TypeField):
                continue

            if id:
                setattr(self, field, val)
            else:
                init_vals[field] = val.value         

        if not id:
            super(Model, self).__init__(**init_vals)

    def __setattr__(self, key, val):
        if hasattr(self, key):
            field = getattr(self, key)
            field.value = val
            if isinstance(field, TypeField):
                self.setProperty(key, val)
            elif isinstance(field, RelationField):
                self.drawRelation(field.relation, val)                
        else:
            object.__setattr__(self, key, val)
   
    def save(self):
        pass

