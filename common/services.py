from .dal import BaseDataAccessLayer

class ServiceBaseClass(object):
    dal_class = BaseDataAccessLayer
    dal = None
    
    def get_list(self, **kwargs):
        return self.dal.get_list(**kwargs)
    
    def get_object(self, pk=None, **kwargs):
        return self.dal.get_object(pk, **kwargs)
    
    def update_object(self, pk, data, partial=False, **kwargs):
        return self.dal.update_object(pk, data, partial, **kwargs)
    
    def create_object(self, data, **kwargs):
        return self.dal.create_object(data, **kwargs)
    
    def delete_object(self, pk, **kwargs):
        return self.dal.delete_object(pk, **kwargs)
    
    def data(self, instance, many=False):
        return self.dal.data(instance, many)