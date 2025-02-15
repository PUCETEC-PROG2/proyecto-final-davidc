from abc import ABC, abstractmethod

class EstadoPropiedad(ABC):
    @abstractmethod
    def cambiar_estado(self, propiedad):
        pass

class EstadoDisponible(EstadoPropiedad):
    def cambiar_estado(self, propiedad):
        propiedad.estado = 'vendido'
        propiedad.save()
        return True

class EstadoVendido(EstadoPropiedad):
    def cambiar_estado(self, propiedad):
        return False