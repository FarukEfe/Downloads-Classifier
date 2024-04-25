class DestinationHandler:

    data = {}
    
    def set_destination(self, format:str, dest:str):
        self.data[format] = dest
    
    def get_destination(self, format:str) -> str:
        try:
            return self.data[format]
        except:
            return None
    
